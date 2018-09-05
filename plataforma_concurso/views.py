from django.shortcuts import render
<<<<<<< HEAD
from django.urls import reverse
=======
from django.http import HttpResponse, HttpResponseBadRequest
import json
>>>>>>> andres

# Create your views here.
from concursos.models import VideoRelacionado
from plataforma_concurso.forms import ParticipanteForm


def index(request):
    return render(request, 'detalle_concurso.html')

def videos(request):
    return render(request, 'videos_concurso.html')

def formulario_participante(request):
    form = ParticipanteForm()
    return render(request, 'formulario_participante.html', {'form': form})

<<<<<<< HEAD
def concurso(request, idconcurso):
    my_url = reverse(concurso, args=(idconcurso,))
    tag = idconcurso
    context = {"my_url": my_url, "concurso": tag};
    return render(request, 'detalle_concurso.html', context)

def concurso_videos(request, idconcurso):
    my_url = reverse(concurso, args=(idconcurso,))
    tag = idconcurso
    context = {"my_url": my_url, "concurso": tag};
    return render(request, 'videos_concurso.html', context)
=======
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
>>>>>>> andres
