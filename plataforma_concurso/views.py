from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest
import json


# Create your views here.
from concursos.models import Concurso, VideoRelacionado, Participante, ParticipanteVideo, EstadosVideoOpciones
from plataforma_concurso.forms import ParticipanteForm


def index(request):
    return render(request, 'detalle_concurso.html')

def videos(request):
    return render(request, 'videos_concurso.html')

def formulario_participante(request):
    form = ParticipanteForm()
    return render(request, 'formulario_participante.html', {'form': form})

def concurso(request, idconcurso):
    my_url = reverse(concurso, args=(idconcurso,))
    url_concurso = idconcurso

    concursos = []

    concursos = Concurso.objects.filter(url = url_concurso )[:1]

    context = {
        "my_url": my_url,
        "url_concurso": url_concurso,
        "concurso": concursos
    };

    if len(concursos) > 0:
        return render(request, 'detalle_concurso.html', context)
    else:
        return render(request, 'error_concurso.html', context)

def concurso_videos(request, idconcurso):
    my_url = reverse(concurso, args=(idconcurso,))
    url_concurso = idconcurso

    concursos = []
    videos = []

    concursos = Participante.objects.filter(concurso__url = url_concurso )

    temp_conc = Concurso.objects.filter(url=idconcurso)

    nombre_concurso = temp_conc[0].nombre

    for x in concursos:
        video = ParticipanteVideo.objects.filter(participante_id = x.id)

        for vid in video:
            conv = VideoRelacionado.objects.filter(id = vid.id, estado ="Procesado")
            for t in conv:
                temp ={}
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

    context = {
        "my_url": my_url,
        "url_concurso": url_concurso,
        "concurso": nombre_concurso,
        "participantes": concursos,
        "videos": videos

    };

    if len(concursos) > 0:
        print("concurso encontrado ", url_concurso, concursos)
        return render(request, 'videos_concurso.html', context)
    else:
        print("concurso NO encontrado", url_concurso)
        return render(request, 'videos_concurso.html', context)

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
        file = request.FILES[u'files']

        # creates the new document
        vr = VideoRelacionado()
        vr.video = file
        vr.save()

        #Se obtienen los datos del archivo creado
        wrapped_file = UploadedFile(vD.archivo)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size

        documentoCrear = Documento()
        formulario = DocumentoForm(request.POST, instance=documentoCrear)

        if formulario.is_valid():
            documentoCrear.versionActual= vD
            formulario.save()
            documentoCrear.versiones.add(vD)
            documentoCrear.save()
             #generating json response array
            files = []
            files.append({
                "name":filename,
                "size":file_size,
                "url":vD.archivo.url,
                "thumbnail_url":vD.archivo.url,
                "delete_url": '',
                "delete_type":"POST",
                #'type': mimetypes.guess_type(file.path)[0] or 'image/png',
            })
            data = {'files': files}
            response = JSONResponse(data, mimetype=response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return HttpResponse(response, mimetype='application/json')
        else:
            return HttpResponse(json.dumps({"success": False, "response":"Formulario Invalido", 'errors': formulario.errors}), content_type="application/json", status=500)
