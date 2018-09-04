from django.db import models
from concursos.models import VideoRelacionado

# Create your models here.
class LogConversion(models.Model):
	video = models.ForeignKey(VideoRelacionado, on_delete=models.DO_NOTHING) # el id del video original
	mensaje = models.CharField(max_length=255) # el mensaje del log
	created_at = models.DateTimeField(auto_now_add=True) #la fecha de creación del log

	class Meta:
		verbose_name = 'Log Conversión'
		verbose_name_plural = 'Log Conversión'
		db_table = 'log_conversion'

	def __str__(self):
		return '%s' % (self.nombre)

class Proceso(models.Model):
	nombre = models.CharField(max_length=255)  # el nombre del proceso
	maquina = models.CharField(max_length=255)  # la máquina que ejecuta el proceso
	started_at = models.DateTimeField(auto_now_add=True) #la fecha-hora de inicio del proceso
	finished_at= models.DateTimeField(auto_now_add=False) #la fecha-hora de finalización del proceso
	created_at = models.DateTimeField(auto_now_add=True) #la fecha de creación del log

	class Meta:
		verbose_name = 'Proceso'
		verbose_name_plural = 'Procesos'
		db_table = 'proceso'

	def __str__(self):
		return '%s' % (self.nombre)