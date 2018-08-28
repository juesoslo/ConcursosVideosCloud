from rest_framework import viewsets
from concursos.models import VideoRelacionado
from plataforma_concurso.serializers import VideoRelacionadoSerializer


class RelatedImageAJAXView(viewsets.ModelViewSet):
    serializer_class = VideoRelacionadoSerializer
    queryset = VideoRelacionado.objects.all()
