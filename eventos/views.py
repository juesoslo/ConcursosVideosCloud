from django.shortcuts import render, render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from .models import Evento

def crear_url_automatica( ):
    unique_id = get_random_string(length=6)
    url_unica = 'concurso'+unique_id
    return url_unica

# Create your views here.
def login_ini(request):
    return render(request, 'eventos/login.html')

def login_view(request):
    if request.method == "POST":
        errors = []
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        next = request.POST.get('next', '')

        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Verify variable context
            return HttpResponseRedirect('/concursos')

        else:
            # Show an error page
            errors.append('Lo sentimos, nombre de usuario o contraseña no válidos.')

            return render(request, 'eventos/landing.html', {'errors': errors, 'username': username})
    else:
        return render(request, 'eventos/landing.html')

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return render(request, 'eventos/landing.html')



def registro_view(req):
    return render(req, 'eventos/signup-step2.html', {'STATIC_URL': settings.STATIC_URL})

def precios_view(req):
    return render(req, 'eventos/signup-step1.html', {'STATIC_URL': settings.STATIC_URL})

def registrar(request):
    errors = []
    nombres = request.POST.get('nombres', '')
    apellidos = request.POST.get('apellidos', '')
    username = request.POST.get('email', '')
    password = request.POST.get('password', '')
    password_confirm = request.POST.get('password_confirm', '')

    search = User.objects.filter(username=username).count()

    if search > 0:
        # Verify variable context
        errors.append('El e-mail ingresado ya se encuentra registrado.')
        return render(request, 'eventos/signup-step2.html', {'errors': errors, 'username' : username})
    elif password != password_confirm:

        # Show an error page
        errors.append('Las contraseñas ingresadas no coinciden.')
        return render(request, 'eventos/signup-step2.html', {'errors': errors})
    else:

        user = User.objects.create_user(first_name=nombres, last_name=apellidos, username=username,
                                 email=username,
                                 password=password)

        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Verify variable context
            errors.append('Tu cuenta se ha creado exitosamente.')
            #return render(request, 'concursos/index.html', context )
            return HttpResponseRedirect('/concursos', {'success': errors})
        else:
            errors.append('Tu cuenta se ha creado exitosamente.')
            return render(request, 'eventos/signup-step2.html', {'success': errors})

def landing(request):
    return render(request, 'eventos/landing.html')

@login_required
def index(request):
    return render(request, 'concursos/index.html')

@login_required
def home(req):
    url_unica = crear_url_automatica()
    context = {
        'STATIC_URL': settings.STATIC_URL,
        "url_unica": url_unica
    };
    return render(req, 'concursos/index.html', context)
    #return render(req, 'concursos/index.html', {'STATIC_URL': settings.STATIC_URL})
    #return render(req, 'eventos/index.html', {'STATIC_URL': settings.STATIC_URL})


@login_required
def get_eventos(request):
    if request.is_ajax():
        q = request.GET.get('username', '')

        eventos = []

        eventos = Evento.objects.filter(usuario = q ).order_by('-created_at')

    context = {
        "search_text": q,
        "mis_eventos": eventos
    };

    #return render(request, 'balance/cds.html', context)
    return  render_to_response("eventos/search_mis_eventos__html_snippet.txt",
                               context)

@login_required
def get_evento(request):
    if request.is_ajax():
        q = request.GET.get('id_event', '')
        tipo_peticion = request.GET.get('tipo_peticion', '')

        eventos = []

        eventos = Evento.objects.filter(id = q )

        print('Ajax Id evento' , q)
        print('Tipo peticion' , tipo_peticion)

    context = {
        "search_text": q,
        "mis_eventos": eventos
    };

    if int(tipo_peticion) == 1:
        return  render_to_response("eventos/view_id_evento__html_snippet.txt",
                                   context)
    elif int(tipo_peticion) == 2:
        return  render_to_response("eventos/edit_id_evento__html_snippet.txt",
                                   context)
    elif int(tipo_peticion) == 3:
        return  render_to_response("eventos/delete_id_evento__html_snippet.txt",
                               context)

@login_required
def crear_evento(request):
    errors = []
    if request.method == "POST":
        username = request.POST.get('username_create', '')
        nombre = request.POST.get('nombre', '')
        categoria = request.POST.get('categoria', '')
        lugar = request.POST.get('lugar', '')
        direccion = request.POST.get('direccion', '')
        fec_ini = request.POST.get('fec_ini', '')
        fec_fin = request.POST.get('fec_fin', '')
        tipo_evento = request.POST.get('tipo_evento', '')

        evento = Evento(usuario=username, nombre=nombre, categoria=categoria, lugar=lugar, direccion=direccion, fec_inicio=fec_ini, fec_fin=fec_fin, tipo_evento=tipo_evento)

        result_create = evento.save()

        errors.append('El evento se ha creado correctamente.')


    return render(request, 'eventos/index.html', {'creacion_exitosa': errors})


@login_required
def editar_evento(request):
    errors = []
    if request.method == "POST":
        username = request.POST.get('username_edit', '')
        id_evento =request.POST.get('id_edit_event', '')

        nombre = request.POST.get('nombre', '')
        categoria = request.POST.get('categoria', '')
        lugar = request.POST.get('lugar', '')
        direccion = request.POST.get('direccion', '')
        fec_ini = request.POST.get('fec_ini', '')
        fec_fin = request.POST.get('fec_fin', '')
        tipo_evento = request.POST.get('tipo_evento', '')

        eventos = Evento.objects.filter(id = id_evento )
        for evento in eventos:
            print(evento.usuario, username)
            if username == evento.usuario:
                evento.nombre = nombre
                evento.categoria = categoria
                evento.lugar = lugar
                evento.direccion = direccion
                evento.fec_inicio = fec_ini
                evento.fec_fin = fec_fin
                evento.tipo_evento = tipo_evento

                result_update = evento.save()

                errors.append('El evento se ha actualizado correctamente.')
            else:
                errors.append('No ha sido posible actualizar el evento.')


    return render(request, 'eventos/index.html', {'edicion_exitosa': errors})



@login_required
def eliminar_evento(request):
    errors = []
    if request.method == "POST":
        username = request.POST.get('username_delete', '')
        id_evento =request.POST.get('id_delete_event', '')

        print('Id evento' , id_evento)

        result_delete = Evento.objects.filter(usuario = username, id=id_evento).delete()

        print('Result delete: ', result_delete[0])

        if result_delete[0] == 0:
            # Verify variable context
            errors.append('No ha sido posible eliminar el evento.')
            return render(request, 'eventos/index.html', {'msj_delete': errors})
        else:
            errors.append('El evento ha sido eliminado exitosamente.')
            return render(request, 'eventos/index.html', {'msj_delete': errors})
    else:
        return render(request, 'eventos/index.html')
