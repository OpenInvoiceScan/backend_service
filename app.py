from flask import Flask, request, jsonify
from flask_cors import CORS
from pdf import save_pdf
import fitz
from PIL import Image
import os
import libraries.processing_pipeline as pp

app = Flask(__name__)
app.debug = True

CORS(app)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/pdf_upload", methods=["POST"])
def pdf_upload():
    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('files')
    
    pdf_routes = save_pdf(files)
    response = ""
    
    for pdf_route in pdf_routes:
        pdf_path = pdf_route["path"]
        response = pp.process_pdf(pdf_path)
        
    
    return response

if __name__ == '__main__':
    app.run()