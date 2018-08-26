from django.db import models

# Create your models here
class Concurso(models.Model):
    nombre		= models.CharField(max_length=255) 					#el nombre del concurso
    banner		= models.ImageField(upload_to='static', null=True)	#el banner o imagen del concurso
    url			= models.CharField(max_length=255) 					#la URL única a todo el sistema
    fec_inicio	= models.DateField()								#la  fecha  de  inicio  del  concurso
    fec_fin		= models.DateField()								#la  fecha  de  fin  del concurso
    descripcion	= models.CharField(max_length=255) 					#la  descripción  del  premio  que  ganará  el  mejor  video
    usuario		= models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'concurso'
        verbose_name_plural = 'concursos'
        db_table='concurso'

    def __str__(self):
        return '%s' % (self.nombre)