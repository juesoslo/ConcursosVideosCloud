from django.contrib import admin

from .models import Concurso, VideoRelacionado, Participante, ParticipanteVideo

# Register your models here.
admin.site.register(Concurso)
admin.site.register(VideoRelacionado)
admin.site.register(Participante)
admin.site.register(ParticipanteVideo)

# Se registran los logs de sesion
from django.contrib.sessions.models import Session
from django.contrib.admin import ModelAdmin


class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)
