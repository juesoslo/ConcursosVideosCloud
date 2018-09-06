from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from plataforma_concurso import views
from .ajax_views import RelatedImageAJAXView

ajax_router = DefaultRouter()
ajax_router.register(r'', RelatedImageAJAXView)

urlpatterns = [
    re_path(r'^(?P<idconcurso>[\w]+)/$', views.index, name='platform_index'),
    re_path(r'^(?P<idconcurso>[\w]+)/videos/$', views.videos, name='platform_videos'),
    re_path(r'^(?P<idconcurso>[\w]+)/nuevo/$', views.formulario_participante, name='platform_form'),
    path('upload', views.video_upload, name='platform_upload'),
    path('api/videos_relacionados/', include(ajax_router.urls)),
]
