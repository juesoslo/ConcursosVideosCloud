from rest_framework import serializers
from concursos.models import VideoRelacionado


class VideoRelacionadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoRelacionado
        fields = ('id', 'video', 'estado')
