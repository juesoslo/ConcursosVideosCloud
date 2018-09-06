import json
from rest_framework import serializers
#from .models import indicador
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

#class indicadorSerializer(serializers.ModelSerializer):
#	class Meta:
#		model = indicador
#		fields = '__all__'
#		fields = ('id_indicador','nombre_indicador','actividad_economica')


class modeloJSON(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(modeloJSON, self).__init__(content, **kwargs)
