import os
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
from io import BytesIO


def save_pdf(files):
    results = []
    for file in files:
        if file.filename == '':
            continue
        if file and file.filename.endswith('.pdf'):
            try:
                # Guardar el archivo PDF
                pdf_path = os.path.join("temp", file.filename)
                file.save(pdf_path)
                # Agregar la ruta relativa al resultado
                results.append({"filename": file.filename, "path": pdf_path})

            except Exception as e:
                results.append({"filename": file.filename, "error": str(e)})
        else:
            results.append({"filename": file.filename, "error": "Invalid file type, only PDF is allowed"})
    return results



def pdf_to_img(pdf_path, dpi=300):
    # Convertir el PDF a imágenes
    pages = convert_from_path(pdf_path, dpi)
    
    # Convertir la primera página a un array de NumPy
    image = pages[0]
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Convertir la imagen a un array de NumPy
    image_np = np.array(Image.open(BytesIO(img_byte_arr)))

    return image_np
