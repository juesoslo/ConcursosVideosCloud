from django.urls import include, path
from rest_framework.routers import DefaultRouter

from plataforma_concurso import views
from .ajax_views import RelatedImageAJAXView

ajax_router = DefaultRouter()
ajax_router.register(r'', RelatedImageAJAXView)

urlpatterns = [
    path('', views.index, name='platform_index'),
    path('videos/', views.videos, name='platform_videos'),
    path('nuevo/', views.formulario_participante, name='platform_form'),
    path('api/videos_relacionados/', include(ajax_router.urls)),
]