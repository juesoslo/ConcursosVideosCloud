from django.shortcuts import render
from .serializers import modeloJSON
from django.conf import settings
from concursos.models import VideoRelacionado, EstadosVideoOpciones
from django.utils.crypto import get_random_string
import subprocess

# Create your views here.
def convertir_videos(request):

	#Consultar los videos pendientes de procesar
	videos = VideoRelacionado.objects.filter(estado = EstadosVideoOpciones.TODO.value )

	#Recorrer los videos pendientes
	for video in videos:
		convertir_video(video)

	return modeloJSON("ok")

def convertir_video( video ):
	#La URL del Video original
	video_original = str(video.video)
	
	#Revisando si la extensión del video ya es .mp4
	extension_video = video_original[-4:].lower()

	#Si la extensión del video ya es .mp4, se asume que el video ya está convertido
	if extension_video == '.mp4':
		video.video_convertido = video.video #El video convertido es el mismo video original
		video.estado = EstadosVideoOpciones.DONE.value #El estado del video es DONE
		video.save()
		return True
		
	#Si la extensión del video NO es .mp4, se convierte el video
	else:
		#Formando la URL con la que quedará el Video convertido
		random_string = get_random_string(length=6)
		video_convertido = video_original.replace("videos/", "videos/convertidos/"+random_string) #Se agrega a la url el /convertidos
		video_convertido = video_convertido+".mp4" #Se agrega la extensión .mp4

		#Se intenta convertir el video
		convertido = convertir_video_con_aplicacion_externa( settings.MEDIA_ROOT+video_original, settings.MEDIA_ROOT+video_convertido )
		if convertido is True:
			video.video_convertido = video_convertido #El video convertido es el mismo video original
			video.estado = EstadosVideoOpciones.DONE.value #El estado del video es DONE
			video.save()
			return True

		else:
			video.estado = EstadosVideoOpciones.ERROR.value #El estado del video es DONE
			video.save()
			return False


def convertir_video_con_aplicacion_externa( video_original, video_convertido ):
	return_value = subprocess.call([
	    'ffmpeg',
	    '-i', video_original,
	    '-strict', '-2',
	    video_convertido,
	])

	if return_value:
	    return False
	else:
	    return True