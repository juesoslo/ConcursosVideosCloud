from django.db import models
from concursos.models import VideoRelacionado

# Create your models here.
class LogConversion(models.Model):
	video = models.CharField(max_length=255, null=True) # el id del video original
	mensaje = models.CharField(max_length=255, null=True) # el mensaje del log
	maquina = models.CharField(max_length=255, null=True)  # la máquina que ejecuta el proceso
	created_at = models.DateTimeField(auto_now_add=True) #la fecha de creación del log

	class Meta:
		verbose_name = 'Log Conversión'
		verbose_name_plural = 'Log Conversión'
		db_table = 'log_conversion'

	def __str__(self):
		return str(self.created_at) +' - '+ str(self.video) +' - '+ self.maquina +' - '+ self.mensaje

class Proceso(models.Model):
	nombre = models.CharField(max_length=255)  # el nombre del proceso
	maquina = models.CharField(max_length=255)  # la máquina que ejecuta el proceso
	started_at = models.DateTimeField(auto_now_add=True, blank=True, null=True) #la fecha-hora de inicio del proceso
	finished_at= models.DateTimeField(auto_now_add=False, default=None, blank=True, null=True) #la fecha-hora de finalización del proceso

	class Meta:
		verbose_name = 'Proceso'
		verbose_name_plural = 'Procesos'
		db_table = 'proceso'

	def __str__(self):
		return self.nombre +' - '+ self.maquina +' - Inicio: '+ str(self.started_at) +' - Fin: '+ str(self.finished_at)