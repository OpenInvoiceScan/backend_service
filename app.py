from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from libraries.pdf import save_pdf
from PIL import Image
import os
import libraries.processing_pipeline as pp
import libraries.pdf_signer as ps
import json
import io
import zipfile


app = Flask(__name__)
app.debug = True

CORS(app)



@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/pdf_upload/json", methods=["POST"])
def pdf_upload_json():
    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('files')
    
    pdf_routes = save_pdf(files)
    response = ""
    
    for pdf_route in pdf_routes:
        pdf_path = pdf_route["path"]
        response = pp.process_pdf(pdf_path)
        
    return response

@app.route("/pdf_upload/signed_pdf", methods=["POST"])
def pdf_upload_signed_pdf():
    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('files')
    
    pdf_routes = save_pdf(files)
    response = ""
    result = []
    
    for pdf_route in pdf_routes:
        pdf_path = pdf_route["path"]
        response = pp.process_pdf(pdf_path)
        ps.add_metadata(response, pdf_path)
        result.append(pdf_path)

    ##Send a zip file with the signed pdfs
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for pdf_path in result:
            zip_file.write(pdf_path, os.path.basename(pdf_path))
    zip_buffer.seek(0)

    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='signed_pdfs.zip')


@app.route('/download_test_pdf', methods=['GET'])
def download_test_pdf():
    test_pdf_path = 'template1.pdf'
    if os.path.exists(test_pdf_path):
        return send_file(test_pdf_path, mimetype='application/pdf', as_attachment=True, download_name='test.pdf')
    else:
        return jsonify({"error": "Test PDF not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)