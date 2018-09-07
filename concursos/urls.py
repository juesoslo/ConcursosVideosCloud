from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/get_concursos/', views.get_concursos, name='get_concursos'),
    path('api/get_concurso/', views.get_concurso, name='get_concurso'),
    path('crear', views.crear_concurso, name='crear_concurso'),
    path('editar', views.editar_concurso, name='editar_concurso'),
    path('eliminar', views.eliminar_concurso, name='eliminar_concurso'),
]
