import requests
import json

url = "http://localhost:5000/pdf_upload"  # Cambia esto a la URL correcta de tu aplicación

files = {
    'files': ('factura69.pdf', open('factura69.pdf', 'rb'), 'application/pdf')
}

response = requests.post(url, files=files)

print(json.dumps(response.json(), indent=4))