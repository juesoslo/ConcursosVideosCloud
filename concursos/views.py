from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Concurso, Participante, ParticipanteVideo, VideoRelacionado

def crear_url_automatica( ):
    maximo_intentos = 10
    intentos = 1
    while True:
        unique_id = get_random_string(length=6)
        url_unica = 'concurso'+unique_id

        intentos += 1
        if es_url_unica(url_unica) or intentos > maximo_intentos:
            break

    return url_unica

@login_required
def index(request):
    url_unica = crear_url_automatica()
    return render(request, 'concursos/index.html', {"url_unica": url_unica})

@login_required
def home(req):
    url_unica = crear_url_automatica()
    context = {
        'STATIC_URL': settings.STATIC_URL,
        "url_unica": url_unica
    };
    return render(req, 'concursos/index.html', context)


@login_required
def get_concursos(request):
    q = ''
    concursos = []
    if request.is_ajax():
        q = request.GET.get('username', '')
        concursos = Concurso.objects.filter(usuario = q ).order_by('-created_at')

    context = {
        "search_text": q,
        "mis_concursos": concursos
    };

    #return render(request, 'balance/cds.html', context)
    return  render_to_response("concursos/search_mis_concursos__html_snippet.txt",
                               context)

@login_required
def get_concurso(request):
    q = ''
    nombre_concurso = ''
    concursos = []
    videos = []
    if request.is_ajax():
        q = request.GET.get('id_event', '')
        tipo_peticion = request.GET.get('tipo_peticion', '')
        concursos = Concurso.objects.filter(id = q )

        if int(tipo_peticion) == 4:
            participantes = Participante.objects.filter(concurso__id = q).order_by('-created_at')

            for x in participantes:
                video = ParticipanteVideo.objects.filter(participante_id = x.id)
                nombre_concurso = x.concurso

                for vid in video:
                    conv = VideoRelacionado.objects.filter(id = vid.video.id)
                    for t in conv:
                        temp ={}
                        partic_create = x.created_at
                        partic_id = x.id
                        partic_nombre = x.nombre
                        partic_apellido = x.apellido
                        partic_email = x.email
                        partic_mensaje = x.mensaje
                        video_original = t.video
                        video_convertido = t.video_convertido
                        video_estado = t.estado
                        temp['partic_create'] = partic_create
                        temp['partic_id'] = partic_id
                        temp['partic_nombre'] = partic_nombre
                        temp['partic_apellido'] = partic_apellido
                        temp['partic_email'] = partic_email
                        temp['partic_mensaje'] = partic_mensaje
                        temp['video_original'] = video_original
                        temp['video_convertido'] = video_convertido
                        temp['video_estado'] = video_estado
                        videos.append(temp)

        #print('Ajax Id concurso' , q)
        #print('Tipo peticion' , tipo_peticion)

    context = {
        "search_text": q,
        "mis_concursos": concursos,
        "nombre_concurso": nombre_concurso,
        "videos": videos
    };

    if int(tipo_peticion) == 1:
        return  render_to_response("concursos/view_id_concurso__html_snippet.txt",
                                   context)
    elif int(tipo_peticion) == 2:
        return  render_to_response("concursos/edit_id_concurso__html_snippet.txt",
                                   context)
    elif int(tipo_peticion) == 3:
        return  render_to_response("concursos/delete_id_concurso__html_snippet.txt",
                               context)
    elif int(tipo_peticion) == 4:
            return  render_to_response("concursos/videos_id_concurso__html_snippet.txt",
                               context)

def es_url_unica( url, id_concurso='--vacio--' ):
    concursos = Concurso.objects.filter( url = url ) #Se busca la URL del concurso
    for concurso in concursos: #Recorre los concursos que tienen esa URL
        #Si existe OTRO concurso con esa URL
        if id_concurso == '--vacio--' or ( id_concurso != '--vacio--' and concurso.id != int(id_concurso) ):
            return False #No es URL única

    return True #Es URL única


@login_required
def crear_concurso(request):
    errors = []
    if request.method == "POST":

        #Cargue del banner
        banner = ''
        for f in request.FILES.getlist('banner'):
            banner = f

        username = request.POST.get('username_create', '')
        nombre = request.POST.get('nombre', '')
        url = request.POST.get('url', '')
        fec_ini = request.POST.get('fec_ini', '')
        fec_fin = request.POST.get('fec_fin', '')
        descripcion = request.POST.get('descripcion', '')

        if es_url_unica(url) is False:
            errors.append('La url está en uso. Se asignó automáticamente.')
            url = crear_url_automatica()

        concurso = Concurso(usuario=username,
        					nombre=nombre,
        					banner=banner,
        					url=url,
        					fec_inicio=fec_ini,
        					fec_fin=fec_fin,
        					descripcion=descripcion)

        result_create = concurso.save()

        errors.append('El concurso se ha creado correctamente.')

    url_unica = crear_url_automatica()
    return render(request, 'concursos/index.html', {'creacion_exitosa': errors, "url_unica": url_unica})


@login_required
def editar_concurso(request):
    errors = []
    if request.method == "POST":

        username = request.POST.get('username_edit', '')
        id_concurso =request.POST.get('id_edit_event', '')

        #Cargue del banner
        banner = ''
        for f in request.FILES.getlist('banner'):
            banner = f

        nombre = request.POST.get('nombre', '')
        url = request.POST.get('url', '')
        fec_ini = request.POST.get('fec_ini', '')
        fec_fin = request.POST.get('fec_fin', '')
        descripcion = request.POST.get('descripcion', '')

        concursos = Concurso.objects.filter(id = id_concurso )
        for concurso in concursos:
            #print(concurso.usuario, username)
            if username == concurso.usuario:
                if banner != '': #Sólo cambia el banner si se sube un archivo
                    concurso.banner = banner

                if es_url_unica(url, id_concurso):
                    concurso.url = url
                else:
                    errors.append('URL no actualizada porque ya está en uso.')

                concurso.nombre = nombre
                concurso.fec_inicio = fec_ini
                concurso.fec_fin = fec_fin
                concurso.descripcion = descripcion

                result_update = concurso.save()

                errors.append('El concurso se ha actualizado correctamente.')
            else:
                errors.append('No ha sido posible actualizar el concurso.')

    url_unica = crear_url_automatica()
    return render(request, 'concursos/index.html', {'edicion_exitosa': errors, "url_unica": url_unica})


@login_required
def eliminar_concurso(request):
    errors = []
    if request.method == "POST":
        username = request.POST.get('username_delete', '')
        id_concurso =request.POST.get('id_delete_event', '')

        #print('Id concurso' , id_concurso)

        result_delete = Concurso.objects.filter(usuario = username, id=id_concurso).delete()

        #print('Result delete: ', result_delete[0])

        if result_delete[0] == 0:
            # Verify variable context
            url_unica = crear_url_automatica()
            errors.append('No ha sido posible eliminar el concurso.')
            return render(request, 'concursos/index.html', {'msj_delete': errors, "url_unica": url_unica})
        else:
            url_unica = crear_url_automatica()
            errors.append('El concurso ha sido eliminado exitosamente.')
            return render(request, 'concursos/index.html', {'msj_delete': errors, "url_unica": url_unica})
    else:
        url_unica = crear_url_automatica()
        return render(request, 'concursos/index.html', {"url_unica": url_unica})
