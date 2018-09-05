from django.shortcuts import render
from .serializers import modeloJSON
from django.conf import settings
from concursos.models import VideoRelacionado, EstadosVideoOpciones
from .models import Proceso, LogConversion
from django.utils.crypto import get_random_string
from datetime import datetime 
import socket
import subprocess
import _thread

# Create your views here.
def convertir_videos(request):
	#reset_estados_videos()
	#return modeloJSON("ejecutado")

	#DETIENE EL PROCESAMIENTO si el proceso ya está activo en esta máquina
	if esta_activo_el_proceso():
		return modeloJSON("en ejecucion")

	# Create threads as follows
	try:
	   _thread.start_new_thread( ejecutar_proceso_conversion, () )
	   #ejecutar_proceso_conversion()
	except:
	   print("Error: unable to start thread")

	return modeloJSON("ok")

def ejecutar_proceso_conversion( ):
	#Consultar los videos pendientes de procesar
	videos = VideoRelacionado.objects.filter(estado = EstadosVideoOpciones.TODO.value )

	#print('Videos a convertir: ' +str(videos.count()))

	#Si hay videos pendientes de procesar
	if videos.count() > 0:

		#Registra el inicio del procesamiento
		registrar_inicio_proceso( )

		#Recorrer los videos pendientes
		for video in videos:
			#Convierte el video
			convertir_video(video)

		#Registra el final del procesamiento
		registrar_fin_proceso( )

def reset_estados_videos():
	videos = VideoRelacionado.objects.all()
	for video in videos:
		video_temp = video.video
		video.video_convertido = None
		video.estado = EstadosVideoOpciones.TODO.value
		video.save()

	#for i in range(1, 50):
	#	video_relacionado = VideoRelacionado(video = video_temp)
	#	video_relacionado.save()

def convertir_video( video ):
	registrar_log_conversion( video, 'Inicia el proceso de conversión' )

	#La URL del Video original
	video_original = str(video.video)
	registrar_log_conversion( video, 'URL video original: '+video_original )
	
	#Revisando si la extensión del video ya es .mp4
	extension_video = video_original[-4:].lower()
	registrar_log_conversion( video, 'Extensión del video: '+extension_video )

	#Si la extensión del video ya es .mp4, se asume que el video ya está convertido
	if extension_video == '.mp4':
		registrar_log_conversion( video, 'Se asume el video como ya convertido' )

		video.video_convertido = video.video #El video convertido es el mismo video original
		video.estado = EstadosVideoOpciones.DONE.value #El estado del video es DONE
		video.save()

		registrar_log_conversion( video, 'Termina el proceso de conversión' )
		return True
		
	#Si la extensión del video NO es .mp4, se convierte el video
	else:
		#Formando la URL con la que quedará el Video convertido
		random_string = get_random_string(length=6)
		video_convertido = video_original.replace("videos/", "videos/convertidos/"+random_string) #Se agrega a la url el /convertidos
		video_convertido = video_convertido+".mp4" #Se agrega la extensión .mp4
		registrar_log_conversion( video, 'El video convertido se va a llamar: '+video_convertido )

		#Se intenta convertir el video
		convertido = convertir_video_con_aplicacion_externa( settings.MEDIA_ROOT+video_original, settings.MEDIA_ROOT+video_convertido )
		if convertido is True:
			registrar_log_conversion( video, 'Se actualiza el estado del video a DONE' )
			video.video_convertido = video_convertido #El video convertido es el mismo video original
			video.estado = EstadosVideoOpciones.DONE.value #El estado del video es DONE
			video.save()

			registrar_log_conversion( video, 'Termina el proceso de conversión' )
			return True

		else:
			registrar_log_conversion( video, 'Se actualiza el estado del video a ERROR' )
			video.estado = EstadosVideoOpciones.ERROR.value #El estado del video es DONE
			video.save()

			registrar_log_conversion( video, 'Termina el proceso de conversión' )
			return False


def convertir_video_con_aplicacion_externa( video_original, video_convertido ):
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


def esta_activo_el_proceso( ):
	#Se obtiene la IP de la máquina actual
	maquina = socket.gethostbyname(socket.gethostname())

	#Buscando el proceso que se llama "Conversion" asignado a la máquina actual
	procesos  = Proceso.objects.filter(nombre='Conversion', maquina=maquina )

	#si hay procesos corriendo, se devuelve True
	for proceso in procesos:
		if proceso.finished_at == None:
			return True

	#si no hay procesos corriendo, se devuelve False
	return False


def registrar_inicio_proceso( ):
	#Se obtiene la IP de la máquina actual
	maquina = socket.gethostbyname(socket.gethostname())

	#Buscando el proceso que se llama "Conversion" asignado a la máquina actual
	procesos  = Proceso.objects.filter(nombre='Conversion', maquina=maquina )

	#Si no existe el proceso, lo crea
	if procesos.count() == 0:
		proceso = Proceso(nombre='Conversion', maquina=maquina)
		proceso.started_at  = datetime.now() #Se asigna inicio de proceso
		proceso.finished_at = None #Se borra el final del proceso
		proceso.save()

	#si hay procesos corriendo
	for proceso in procesos:
		#Se actualiza el proceso
		proceso.started_at  = datetime.now() #Se asigna inicio de proceso
		proceso.finished_at = None #Se borra el final del proceso
		proceso.save()


def registrar_fin_proceso( ):
	#Se obtiene la IP de la máquina actual
	maquina = socket.gethostbyname(socket.gethostname())

	#Buscando el proceso que se llama "Conversion" asignado a la máquina actual
	procesos  = Proceso.objects.filter(nombre='Conversion', maquina=maquina )

	#Si no existe el proceso, lo crea
	if procesos.count() == 0:
		proceso = Proceso(nombre='Conversion', maquina=maquina)
		proceso.finished_at = datetime.now() #Se asigna final del proceso
		proceso.save()

	#si hay procesos corriendo
	for proceso in procesos:
		#Se actualiza el proceso
		proceso.finished_at = datetime.now() #Se asigna final del proceso
		proceso.save()


def registrar_log_conversion( video, mensaje ):
	#Se obtiene la IP de la máquina actual
	maquina = socket.gethostbyname(socket.gethostname())

	#Creando el Log de conversión
	log = LogConversion(video=video.id, mensaje=mensaje, maquina=maquina)
	log.save()


