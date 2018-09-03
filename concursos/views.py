from django.shortcuts import render, render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from .models import Concurso

@login_required
def index(request):

    return render(request, 'concursos/index.html')

@login_required
def home(req):
    return render(req, 'concursos/index.html', {'STATIC_URL': settings.STATIC_URL})


@login_required
def get_concursos(request):
    if request.is_ajax():
        q = request.GET.get('username', '')

        concursos = []

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
    if request.is_ajax():
        q = request.GET.get('id_event', '')
        tipo_peticion = request.GET.get('tipo_peticion', '')

        concursos = []

        concursos = Concurso.objects.filter(id = q )

        #print('Ajax Id concurso' , q)
        #print('Tipo peticion' , tipo_peticion)

    context = {
        "search_text": q,
        "mis_concursos": concursos
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

        concurso = Concurso(usuario=username,
        					nombre=nombre,
        					banner=banner,
        					url=url,
        					fec_inicio=fec_ini,
        					fec_fin=fec_fin,
        					descripcion=descripcion)

        result_create = concurso.save()

        errors.append('El concurso se ha creado correctamente.')


    return render(request, 'concursos/index.html', {'creacion_exitosa': errors})


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

                concurso.nombre = nombre
                concurso.url = url
                concurso.fec_inicio = fec_ini
                concurso.fec_fin = fec_fin
                concurso.descripcion = descripcion

                result_update = concurso.save()

                errors.append('El concurso se ha actualizado correctamente.')
            else:
                errors.append('No ha sido posible actualizar el concurso.')


    return render(request, 'concursos/index.html', {'edicion_exitosa': errors})



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
            errors.append('No ha sido posible eliminar el concurso.')
            return render(request, 'concursos/index.html', {'msj_delete': errors})
        else:
            errors.append('El concurso ha sido eliminado exitosamente.')
            return render(request, 'concursos/index.html', {'msj_delete': errors})
    else:
        return render(request, 'concursos/index.html')
