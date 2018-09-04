from django.shortcuts import render
from django.urls import reverse

# Create your views here.
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
    tag = idconcurso
    context = {"my_url": my_url, "concurso": tag};
    return render(request, 'detalle_concurso.html', context)

def concurso_videos(request, idconcurso):
    my_url = reverse(concurso, args=(idconcurso,))
    tag = idconcurso
    context = {"my_url": my_url, "concurso": tag};
    return render(request, 'videos_concurso.html', context)
