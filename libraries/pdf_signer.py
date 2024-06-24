import PyPDF2

def add_metadata(text_input, pdf_route):
    """
    Agrega un metadato personalizado al PDF especificado.

    :param text_input: Texto que se usará como metadato.
    :param pdf_route: Ruta al PDF a firmar.
    """
    with open(pdf_route, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        # Copia todas las páginas del PDF original al nuevo objeto PdfWriter
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)

        # Añade metadatos personalizados
        metadatos = {
            '/AVALON': text_input,
        }

        writer.add_metadata(metadatos)

        # Guarda el nuevo PDF con los metadatos añadidos
        with open(pdf_route, 'wb') as new_file:
            writer.write(new_file)

def check_for_avalon_sign(pdf_route):
    
    with open(pdf_route, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        metadatos = reader.metadata
    
    return '/AVALON' in metadatos
    

def extract_avalon_sign(pdf_route):
    with open(pdf_route, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        metadatos = reader.metadata
    
    return metadatos['/AVALON']


if __name__ == '__main__':
    add_metadata('Clear', 'template1.pdf')
    