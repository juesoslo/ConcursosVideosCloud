import requests

#URL del servicio REST que se va a ejecutar
url = 'http://172.24.42.56:8080/conversion/procesar/'

#Los valores para los parámetros del servicio
data = {}

#Se ejecuta el servicio
response = requests.get(url) #, json=data)


#Se imprime el resultado
print(response.json())