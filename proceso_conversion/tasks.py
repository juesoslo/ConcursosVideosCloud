from __future__ import absolute_import, unicode_literals
from celery import shared_task
from proceso_conversion.views import ejecutar_proceso_conversion_individual


@shared_task
def processVideo(videoId):
    #se llama a proceso de video individual
    ejecutar_proceso_conversion_individual(videoId)

    # # se ejecutan las acciones de procesar video
    #
    # # URL final del aplicativo
    # WEB_URL = os.environ.get("CLOUDG7_WEB_URL", '')
    #
    # # URL del servicio REST que se va a ejecutar
    # url = WEB_URL + '/conversion/procesar/'
    #
    # # Se ejecuta el servicio
    # response = requests.get(url)  # , json=data)
    #
    # # Se imprime el resultado
    # print(response.json())
