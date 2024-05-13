import fitz
from PIL import Image
import os

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

            except Exception as e:
                results.append({"filename": file.filename, "error": str(e)})
        else:
            results.append({"filename": file.filename, "error": "Invalid file type, only PDF is allowed"})
    return results 
