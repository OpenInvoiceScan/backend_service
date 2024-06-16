import requests
import json

url = "http://localhost:5000/pdf_upload/json"  # Cambia esto a la URL correcta de tu aplicación

file = "template2.pdf"

files = {
    'files': (file , open(file, 'rb'), 'application/pdf')
}

response = requests.post(url, files=files)

print(json.dumps(response.json(), indent=4))