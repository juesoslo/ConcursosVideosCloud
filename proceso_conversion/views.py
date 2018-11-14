from django.http import JsonResponse
from proceso_conversion.awsses import sendSESEmail
from .serializers import modeloJSON
from django.conf import settings
from concursos.models import VideoRelacionado, EstadosVideoOpciones, ParticipanteVideo
from .models import Proceso, LogConversion
from django.core.mail import send_mail
from django.utils import timezone
import socket
import subprocess
import _thread
import uuid
import os
from media import media_path as MEDIA_PATH


# Create your views here.
def convertir_videos(request):
    # reset_estados_videos()
    # return modeloJSON("ejecutado")

    # DETIENE EL PROCESAMIENTO si el proceso ya está activo en esta máquina
    if esta_activo_el_proceso():
        return modeloJSON("en ejecucion")

    # Create threads as follows
    try:
        _thread.start_new_thread(ejecutar_proceso_conversion, ())
        # ejecutar_proceso_conversion()
    except:
        print("Error: unable to start thread")

    return modeloJSON("ok")


def ejecutar_proceso_conversion():
    # Consultar los videos pendientes de procesar
    videos = VideoRelacionado.objects.filter(estado=EstadosVideoOpciones.TODO.value)

    # print('Videos a convertir: ' +str(videos.count()))

    # Si hay videos pendientes de procesar
    if videos.count() > 0:

        # Registra el inicio del procesamiento
        registrar_inicio_proceso()

        # Recorrer los videos pendientes
        for video in videos:
            # Convierte el video
            convertir_video(video)

        # Registra el final del procesamiento
        registrar_fin_proceso()


def ejecutar_proceso_conversion_individual(videoId):
    try:
        video = VideoRelacionado.objects.get(id=videoId)
    except VideoRelacionado.DoesNotExist:
        video = None

    if video is not None:
        # registra el inicio del procesamiento
        registrar_inicio_proceso()
        # convierte el video
        convertir_video(video)
        # registra el fin del video
        registrar_fin_proceso()


def reset_estados_videos():
    videos = VideoRelacionado.objects.all()
    for video in videos:
        video_temp = video.video
        video.video_convertido = None
        video.estado = EstadosVideoOpciones.TODO.value
        video.save()


# for i in range(1, 50):
#	video_relacionado = VideoRelacionado(video = video_temp)
#	video_relacionado.save()

def convertir_video(video):
    registrar_log_conversion(video, 'Inicia el proceso de conversión')

    # Actualiza el estado del video a EN PROCESO
    registrar_log_conversion(video, 'Se actualiza el estado del video a DOING')
    video.estado = EstadosVideoOpciones.DOING.value  # El estado del video es DOING
    video.save()

    # La URL del Video original
    video_original = str(video.video)
    registrar_log_conversion(video, 'URL video original: ' + video_original)

    # Revisando si la extensión del video ya es .mp4
    extension_video = video_original[-4:].lower()
    registrar_log_conversion(video, 'Extensión del video: ' + extension_video)

    # Si la extensión del video ya es .mp4, se asume que el video ya está convertido
    if extension_video == '.mp4':
        registrar_log_conversion(video, 'Se asume el video como ya convertido')

        video.video_convertido = video.video  # El video convertido es el mismo video original
        video.estado = EstadosVideoOpciones.DONE.value  # El estado del video es DONE
        video.save()

        # Envía el correo notificando el procesamiento del video
        enviarCorreo(video, EstadosVideoOpciones.DONE.value)

        registrar_log_conversion(video, 'Termina el proceso de conversión')
        return True

    # Si la extensión del video NO es .mp4, se convierte el video
    else:
        # Formando la URL con la que quedará el Video convertido
        video_convertido = get_file_converted_path(video, video.video.url)
        # video_convertido = video_original.replace("videos/", "videos/convertidos/"+random_string) #Se agrega a la url
        # el /convertidos
        # video_convertido = video_convertido+".mp4" #Se agrega la extensión .mp4
        registrar_log_conversion(video, 'El video convertido se va a llamar: ' + video_convertido)

        print("Media path %s" % MEDIA_PATH)

        # Se intenta convertir el video
        convertido = convertir_video_con_aplicacion_externa(os.path.join(settings.MEDIA_URL, video_original),
                                                            video_convertido)
        if convertido is True:
            registrar_log_conversion(video, 'Se actualiza el estado del video a DONE')
            video.video_convertido = video_convertido  # El video convertido es el mismo video original
            video.estado = EstadosVideoOpciones.DONE.value  # El estado del video es DONE
            video.save()

            # Envía el correo notificando el procesamiento del video
            enviarCorreo(video, EstadosVideoOpciones.DONE.value)

            registrar_log_conversion(video, 'Termina el proceso de conversión')
            return True

        else:
            registrar_log_conversion(video, 'Se actualiza el estado del video a ERROR')
            video.estado = EstadosVideoOpciones.ERROR.value  # El estado del video es DONE
            video.save()

            # Envía el correo notificando el procesamiento del video
            enviarCorreo(video, EstadosVideoOpciones.ERROR.value)

            registrar_log_conversion(video, 'Termina el proceso de conversión')
            return False


def get_file_converted_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), 'mp4')
    #makedirs(os.path.join(settings.MEDIA_ROOT, 'videos', str(instance.concurso.id), 'convertidos'))
    #return os.path.join('videos', str(instance.concurso.id), 'convertidos', filename)
    return filename


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == 17:
            # Dir already exists. No biggie.
            pass


def convertir_video_con_aplicacion_externa(video_original, video_convertido):
    print("Salida del video %s" % video_convertido)

    ext = video_original.split('.')[-1]
    if ext == 'mkv':
        return_value = subprocess.call([
            'ffmpeg',
            '-i', video_original,
            '-c', 'copy',
            video_convertido,
        ])
    elif ext == 'flv':
        return_value = subprocess.call([
            'ffmpeg',
            '-i', video_original,
            '-c:a', 'copy',
            '-c:v', 'libx264',
            '-profile:v', 'baseline',
            video_convertido,
        ])
    else:
        return_value = subprocess.call([
            'ffmpeg',
            '-i', video_original,
            '-strict', '-2',
            video_convertido,
        ])

    if return_value:
        return False
    else:
        return True


def esta_activo_el_proceso():
    # Se obtiene la IP de la máquina actual
    maquina = socket.gethostbyname(socket.gethostname())

    # Buscando el proceso que se llama "Conversion" asignado a la máquina actual
    procesos = Proceso.objects.filter(nombre='Conversion', maquina=maquina)

    # si hay procesos corriendo, se devuelve True
    for proceso in procesos:
        if proceso.finished_at == None:
            return True

    # si no hay procesos corriendo, se devuelve False
    return False


def registrar_inicio_proceso():
    # Se obtiene la IP de la máquina actual
    maquina = socket.gethostbyname(socket.gethostname())

    # Buscando el proceso que se llama "Conversion" asignado a la máquina actual
    procesos = Proceso.objects.filter(nombre='Conversion', maquina=maquina)

    # Si no existe el proceso, lo crea
    if procesos.count() == 0:
        proceso = Proceso(nombre='Conversion', maquina=maquina)
        proceso.started_at = timezone.now()  # Se asigna inicio de proceso
        proceso.finished_at = None  # Se borra el final del proceso
        proceso.save()

    # si hay procesos corriendo
    for proceso in procesos:
        # Se actualiza el proceso
        proceso.started_at = timezone.now()  # Se asigna inicio de proceso
        proceso.finished_at = None  # Se borra el final del proceso
        proceso.save()


def registrar_fin_proceso():
    # Se obtiene la IP de la máquina actual
    maquina = socket.gethostbyname(socket.gethostname())

    # Buscando el proceso que se llama "Conversion" asignado a la máquina actual
    procesos = Proceso.objects.filter(nombre='Conversion', maquina=maquina)

    # Si no existe el proceso, lo crea
    if procesos.count() == 0:
        proceso = Proceso(nombre='Conversion', maquina=maquina)
        proceso.finished_at = timezone.now()  # Se asigna final del proceso
        proceso.save()

    # si hay procesos corriendo
    for proceso in procesos:
        # Se actualiza el proceso
        proceso.finished_at = timezone.now()  # Se asigna final del proceso
        proceso.save()


def registrar_log_conversion(video, mensaje):
    # Se obtiene la IP de la máquina actual
    maquina = socket.gethostbyname(socket.gethostname())

    # Creando el Log de conversión
    log = LogConversion(video=video.id, mensaje=mensaje, maquina=maquina)
    log.save()


def enviarCorreo(video, estadoConversion):
    # print('Entra a enviar correo: ' +str(video)+ ' --- ' +estadoConversion)

    # Buscando el participante correspondiente al video
    participantes = ParticipanteVideo.objects.filter(video=video)

    # print('participantes: ' +str(participantes.count()) )

    # si hay participantes con este video
    for participante in participantes:
        # Almacena el email del participante
        destinatario = participante.participante.email

        if (destinatario and estadoConversion):
            # print('envia el email a '+destinatario+ ' y estado: '+estadoConversion)
            mensaje = ''
            if estadoConversion == EstadosVideoOpciones.DONE.value:
                mensaje = 'El video ya ha sido publicado en la página del concurso.'

            try:
                send_mail(
                    'Conversión de video terminada: ' + estadoConversion,
                    """
                    El proceso de conversion de su video ha terminado con estado: {0}. {1}
                    Concurso: {2}
                    Url de Acceso: {4}/platform/{3}
                    """.format(estadoConversion, mensaje, participante.participante.concurso.nombre,
                               participante.participante.concurso.url, settings.WEB_URL),
                    'Smartools.com <no-reply@smartools.com>',
                    [destinatario],
                    fail_silently=False,
                )
                # sendSESEmail(
                #     'Conversión de video terminada: ' + estadoConversion,
                #     'El proceso de conversión de su video ha terminado con estado: ' + estadoConversion + mensaje,
                #     [destinatario]
                # )
            except:
                pass

    return True


def enviarSESCorreo(request):
    sendSESEmail('Prueba', 'Notificacion de prueba', ['ad.betin@uniandes.edu.co'])
    return JsonResponse({'result': True})
