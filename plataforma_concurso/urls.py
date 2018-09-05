from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from plataforma_concurso import views
from .ajax_views import RelatedImageAJAXView

ajax_router = DefaultRouter()
ajax_router.register(r'', RelatedImageAJAXView)

urlpatterns = [
    path('', views.index, name='platform_index'),
    re_path(r'^concurso/(?P<idconcurso>[\w]+)/$', views.concurso, name='platform_concurso'),
    re_path(r'^concurso/(?P<idconcurso>[\w]+)/videos/$', views.concurso_videos, name='platform_concurso1232'),
    path('videos/', views.videos, name='platform_videos'),
    path('nuevo/', views.formulario_participante, name='platform_form'),
    path('api/videos_relacionados/', include(ajax_router.urls)),
<<<<<<< HEAD
]
=======
    path('upload', views.video_upload, name='platform_upload'),
]
>>>>>>> andres
