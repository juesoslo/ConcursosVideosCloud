from django.urls import path
from . import views

urlpatterns = [
    # path('', views.login_ini, name='login'),
    path('', views.landing, name='landing'),
    path('accounts/login/', views.login_view),
    path('account/loggedin', views.index),
    path('accounts/logout', views.logout_view),
    path('registro/', views.registro_view, name='registro'),
    path('registro/new', views.registrar, name='registrar'),
    path('home/', views.home, name='home'),
    path('api/get_eventos/', views.get_eventos, name='get_eventos'),
    path('api/get_evento/', views.get_evento, name='get_evento'),
    path('evento/crear', views.crear_evento, name='crear_evento'),
    path('evento/editar', views.editar_evento, name='editar_evento'),
    path('evento/eliminar', views.eliminar_evento, name='eliminar_evento'),
]
