from django.contrib import admin
from concursos.models import Concurso, VideoRelacionado, Participante, ParticipanteVideo

# Register your models here.
admin.site.register(Concurso)
admin.site.register(VideoRelacionado)
admin.site.register(Participante)
admin.site.register(ParticipanteVideo)
