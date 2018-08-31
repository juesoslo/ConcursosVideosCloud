from django.shortcuts import render

# Create your views here.
from plataforma_concurso.forms import ParticipanteForm


def index(request):
    return render(request, 'detalle_concurso.html')

def videos(request):
    return render(request, 'videos_concurso.html')

def formulario_participante(request):
    form = ParticipanteForm()
    return render(request, 'formulario_participante.html', {'form': form})
