import requests

url = "http://localhost:5000/pdf_upload/signed_pdf"  # Cambia esto a la URL correcta de tu aplicación

file = "template2.pdf"

files = {
    'files': (file, open(file, 'rb'), 'application/pdf')
}

response = requests.post(url, files=files)

# Verificar si la respuesta es exitosa
if response.status_code == 200:
    # Guardar el archivo descargado
    with open("downloaded_signed_pdf.pdf", 'wb') as f:
        f.write(response.content)
    print("PDF descargado y guardado como 'downloaded_signed_pdf.pdf'.")
else:
    print("Error al descargar el PDF:", response.status_code)
    print(response.text)
