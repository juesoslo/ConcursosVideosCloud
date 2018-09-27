import requests
import os

#URL final del aplicativo
WEB_URL = os.environ.get("CLOUDG7_WEB_URL", '')

#URL del servicio REST que se va a ejecutar
url = WEB_URL+'/conversion/procesar/'

#Los valores para los parámetros del servicio
data = {}

#Se ejecuta el servicio
response = requests.get(url) #, json=data)


#Se imprime el resultado
print(response.json())