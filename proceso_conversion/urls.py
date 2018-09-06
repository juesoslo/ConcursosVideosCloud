from django.urls import path
from . import views

urlpatterns = [
    path('procesar/', views.convertir_videos, name='convertir_videos'),
]
