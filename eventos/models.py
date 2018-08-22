from django.db import models

# Create your models here
class Evento(models.Model):
     nombre = models.CharField(max_length=255)
     categoria = models.CharField(max_length=15)
     lugar = models.CharField(max_length=255)
     direccion = models.CharField(max_length=150)
     created_at = models.DateTimeField(auto_now_add=True)
     fec_inicio = models.DateField()
     fec_fin = models.DateField()
     tipo_evento = models.CharField(max_length=15)
     usuario = models.CharField(max_length=255)


#Un  evento  está  compuesto  de  un  nombre,  una  categoría  (las  cuatro  posibles categorías  son:
#  Conferencia,  Seminario,  Congreso  o  Curso),  un  lugar,  una  dirección, una  fecha  de inicio
#y una fecha de fin, y si el evento es presencial o virtual
