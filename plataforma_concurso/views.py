from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.core.files.uploadedfile import UploadedFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from concursos.models import Concurso, VideoRelacionado, Participante, ParticipanteVideo, EstadosVideoOpciones
from plataforma_concurso.forms import ParticipanteForm
import boto3
import os


def index(request, idconcurso):
    my_url = reverse(index, args=(idconcurso,))
    concursos = Concurso.objects.filter(url=idconcurso)[:1]

    context = {
        "my_url": my_url,
        "url_concurso": idconcurso,
        "concursos": concursos,
    };

    if len(concursos) > 0:
        context["id_concurso"] = concursos[0].id
        return render(request, 'detalle_concurso.html', context)
    else:
        return render(request, 'error_concurso.html', context)


def videos(request, idconcurso):
    my_url = reverse(index, args=(idconcurso,))
    url_concurso = idconcurso

    concursos = []
    videos = []

    concursos = Participante.objects.filter(concurso__url=url_concurso)

    temp_conc = Concurso.objects.filter(url=idconcurso)

    nombre_concurso = temp_conc[0].nombre

    for x in concursos:
        video = ParticipanteVideo.objects.filter(participante_id=x.id)
        
        for vid in video:
            conv = VideoRelacionado.objects.filter(id=vid.video.id, estado=EstadosVideoOpciones.DONE.value)
            for t in conv:
                temp = {}
                partic_id = x.id
                partic_nombre = x.nombre
                partic_apellido = x.apellido
                partic_email = x.email
                partic_mensaje = x.mensaje
                video_original = t.video
                video_convertido = t.video_convertido
                temp['partic_id'] = partic_id
                temp['partic_nombre'] = partic_nombre
                temp['partic_apellido'] = partic_apellido
                temp['partic_email'] = partic_email
                temp['partic_mensaje'] = partic_mensaje
                temp['video_original'] = video_original
                temp['video_convertido'] = video_convertido
                videos.append(temp)

    page = request.GET.get('page', 1)
    paginator = Paginator(videos, 20)

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    context = {
        "my_url": my_url,
        "url_concurso": url_concurso,
        "concurso": nombre_concurso,
        "participantes": concursos,
        "videos": videos

    }

    if len(concursos) > 0:
        print("concurso encontrado ", url_concurso, concursos)
        return render(request, 'videos_concurso.html', context)
    else:
        print("concurso NO encontrado", url_concurso)
        return render(request, 'videos_concurso.html', context)


def formulario_participante(request, idconcurso):
    my_url = reverse(index, args=(idconcurso,))
    concursos = Concurso.objects.filter(url=idconcurso)[:1]

    context = {
        "my_url": my_url,
        "url_concurso": idconcurso,
        "concursos": concursos,
    };

    if len(concursos) > 0:
        context["id_concurso"] = concursos[0].id
        context["form"] = ParticipanteForm()
        return render(request, 'formulario_participante.html', context)
    else:
        return render(request, 'error_concurso.html', context)


def video_upload(request):
    if request.method == 'POST':
        if request.FILES == None:
            return HttpResponseBadRequest('¡Debe tener archivos!')

        # get the file
        file = request.FILES[u'video']

        # get concurso
        concurso_id = request.POST[u'concurso_id']
        concursos = Concurso.objects.filter(pk=concurso_id)

        if len(concursos) <= 0:
            return HttpResponse(
                json.dumps(
                    {"success": False, "response": "Concurso no encontrado", 'errors': ["Concurso no encontrado"]}),
                content_type="application/json", status=500)

        # creates the new document
        vr = VideoRelacionado(video=file, concurso_id=int(concurso_id))
        vr.save()

        # Se obtienen los datos del archivo creado
        wrapped_file = UploadedFile(vr.video)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size

        files = []
        files.append({
            "name": filename,
            "size": file_size,
            "url": vr.video.url,
        })

        # se crea el participante
        participante_nombre = request.POST[u'participante_nombre']
        participante_apellido = request.POST[u'participante_apellido']
        participante_email = request.POST[u'participante_email']
        participante_mensaje = request.POST[u'participante_mensaje']

        participante = Participante(nombre=participante_nombre, apellido=participante_apellido,
                                    email=participante_email, mensaje=participante_mensaje,
                                    concurso_id=int(concurso_id))
        participante.save()

        # se crea la relacion final
        participanteVideo = ParticipanteVideo(video=vr, participante=participante)
        participanteVideo.save()

        # se inserta mensaje en la cola informando el nuevo video
        insertQueueMessage("Procesar video: " + str(vr.id), vr.id)

        return HttpResponse(
            json.dumps({"success": True, "response": "Cargado con exito", 'errors': [], 'files': files,
                        'Content-Disposition': 'inline; filename=files.json'}),
            content_type="application/json", status=200)
    else:
        return HttpResponse(
            json.dumps({"success": False, "response": "Metodo no permitido", 'errors': ["Metodo no permitido"]}),
            content_type="application/json", status=500)


def insertQueueMessage(message, videoId):

    AWS_REGION = "us-east-2"
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", '')
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", '')

    # Create SQS client
    sqs = boto3.client(
        'sqs',
        region_name=AWS_REGION,
        # Hard coded strings as credentials, not recommended.
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    queue_url = 'https://sqs.us-east-2.amazonaws.com/687383508727/cloudg7-videos-queue'

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'VideoId': {
                'DataType': 'Number',
                'StringValue': str(videoId)
            }
        },
        MessageBody=message
    )
