#!/bin/bash

# Crea el entorno virtual
python3 -m venv .venv

# Activa el entorno virtual
source .venv/bin/activate

# Actualiza pip a la última versión
pip install --upgrade pip

# Instala las dependencias externas
pip install opencv-python-headless \
            pdf2image \
            torch \
            transformers \
            scikit-learn \
            PyPDF2 \
            numpy \
            flask \
            flask-cors \
            fitz 

# Desactiva el entorno virtual
deactivate

echo "Dependencias externas instaladas exitosamente en el entorno virtual .venv"
