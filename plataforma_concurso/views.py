from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.core.files.uploadedfile import UploadedFile

# Create your views here.
from concursos.models import Concurso, VideoRelacionado, Participante, ParticipanteVideo
from plataforma_concurso.forms import ParticipanteForm


def videos(request):
    return render(request, 'videos_concurso.html')

def formulario_participante(request):
    form = ParticipanteForm()
    return render(request, 'formulario_participante.html', {'form': form})

def index(request, idconcurso):
    my_url = reverse(index, args=(idconcurso,))
    url_concurso = idconcurso
    concursos = Concurso.objects.filter(url=url_concurso)[:1]

    context = {
        "my_url": my_url,
        "url_concurso": url_concurso,
        "concurso": concursos,
    };

    if len(concursos) > 0:
        context["id_concurso"] = concursos[0]
        return render(request, 'detalle_concurso.html', context)
    else:
        return render(request, 'error_concurso.html', context)

def concurso_videos(request, idconcurso):
    my_url = reverse(index, args=(idconcurso,))
    url_concurso = idconcurso

    concursos = []
    videos = []

    concursos = Participante.objects.filter(concurso__url = url_concurso )

    for x in concursos:
        video = ParticipanteVideo.objects.filter(participante_id = x.id)
        print(video)
        for vid in video:
            conv = VideoRelacionado.objects.filter(id=vid.id)
            for t in conv:
                temp ={}
                part = x.id
                vid = t.video_convertido
                temp['part'] = part
                temp['vid'] = vid
                videos.append(temp)
                print("video: ",t.video)

    print("Lista de videos ", videos)
    print("Lista de participantes ", concursos)

    context = {
        "my_url": my_url,
        "url_concurso": url_concurso,
        "participantes": concursos,
        "videos": videos
    };

    if len(concursos) > 0:
        print("concurso encontrado ", url_concurso, concursos)
        return render(request, 'videos_concurso.html', context)
    else:
        print("concurso NO encontrado", url_concurso)
        return render(request, 'error_concurso.html', context)

def concurso_participante(request, idconcurso):
    my_url = reverse(concurso, args=(idconcurso,))
    tag = idconcurso
    form = ParticipanteForm()
    context = {"my_url": my_url, "concurso": tag, 'form': form};
    return render(request, 'formulario_participante.html', context)

def video_upload(request):
    if request.method == 'POST':
        if request.FILES == None:
            return HttpResponseBadRequest('¡Debe tener archivos!')

        # get the file
        file = request.FILES[u'video']

        # creates the new document
        vr = VideoRelacionado()
        vr.video = file
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

        return HttpResponse(
            json.dumps({"success": True, "response": "Cargado con exito", 'errors': [], 'files': files,
                        'Content-Disposition': 'inline; filename=files.json'}),
            content_type="application/json", status=200)
    else:
        return HttpResponse(
            json.dumps({"success": False, "response": "Metodo no permitido", 'errors': ["Metodo no permitido"]}),
            content_type="application/json", status=500)
