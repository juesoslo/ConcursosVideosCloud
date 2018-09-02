from enum import Enum
from django.db import models


# Create your models here
class Concurso(models.Model):
    nombre = models.CharField(max_length=255)  # el nombre del concurso
    banner = models.ImageField(upload_to='banners/', null=True)  # el banner o imagen del concurso
    url = models.CharField(max_length=255)  # la URL única a todo el sistema
    fec_inicio = models.DateField()  # la  fecha  de  inicio  del  concurso
    fec_fin = models.DateField()  # la  fecha  de  fin  del concurso
    descripcion = models.CharField(max_length=255)  # la  descripción  del  premio  que  ganará  el  mejor  video
    usuario = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'concurso'
        verbose_name_plural = 'concursos'
        db_table = 'concurso'

    def __str__(self):
        return '%s' % (self.nombre)


class EstadosVideoOpciones(Enum):  # A subclass of Enum
    TODO = "Por Hacer"
    DOING = "En progreso"
    DONE = "Procesado"
    ERROR = "Error al procesar"


class VideoRelacionado(models.Model):
    video = models.FileField(upload_to='videos/')
    estado = models.CharField(
        max_length=10,
        choices=[(tag, tag.value) for tag in EstadosVideoOpciones],
        default=EstadosVideoOpciones.TODO
    )

    class Meta:
        verbose_name = 'video relacionado'
        verbose_name_plural = 'videos relacionados'
        db_table = 'video_relacionado'

    def __unicode__(self):
        return self.video.url


class Participante(models.Model):
    nombre = models.CharField(max_length=255)  # el nombre del participante
    apellido = models.CharField(max_length=255)  # el apellido del participante
    email = models.EmailField(max_length=255)  # el correo del participante
    mensaje = models.TextField()  # mensaje relacionado con el video
<<<<<<< HEAD
    concurso = models.ForeignKey(Concurso, on_delete=models.PROTECT)
=======
    concurso = models.ForeignKey(Concurso, on_delete=models.PROTECT, related_name='participantes')
>>>>>>> andres
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'participante'
        verbose_name_plural = 'participantes'
        db_table = 'participante'

    def __str__(self):
        return '%s %s' % (self.nombre, self.apellido)


class ParticipanteVideo(models.Model):
    video = models.ForeignKey(VideoRelacionado, on_delete=models.PROTECT)
    participante = models.ForeignKey(Participante, on_delete=models.PROTECT)
