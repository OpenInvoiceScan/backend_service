from pdf2image import convert_from_path
import cv2
import numpy as np


## Función para el pipeline para la extracción de filas de una tabla
def merge_boxes_on_same_row(boxes, y_threshold):
    # Ordenar las bounding boxes por la coordenada y
    boxes.sort(key=lambda b: b[1])

    def get_y_center(box):
        _, y, _, h = box
        return y + h // 2

    # Agrupar las bounding boxes
    grouped_boxes = []
    current_group = []

    for box in boxes:
        if not current_group:
            current_group.append(box)
        else:
            last_box = current_group[-1]
            if abs(get_y_center(box) - get_y_center(last_box)) <= y_threshold:
                current_group.append(box)
            else:
                # Si no se agrupan, comprobar si el grupo actual tiene 4 o más elementos
                if len(current_group) >= 4:
                    grouped_boxes.append(current_group)
                current_group = [box]

    # Comprobar el último grupo
    if len(current_group) >= 4:
        grouped_boxes.append(current_group)

    # Crear nuevas bounding boxes agrupadas
    merged_boxes = []
    for group in grouped_boxes:
        x_min = min(box[0] for box in group)
        y_min = min(box[1] for box in group)
        x_max = max(box[0] + box[2] for box in group)
        y_max = max(box[1] + box[3] for box in group)
        merged_boxes.append((x_min, y_min, x_max - x_min, y_max - y_min))

    # Incluir las cajas que no fueron agrupadas
    all_grouped_boxes = sum(grouped_boxes, [])
    for box in boxes:
        if box not in all_grouped_boxes:
            merged_boxes.append(box)
    
    # Ordenar las bounding boxes por la coordenada y
    merged_boxes.sort(key=lambda b: b[1])

    return merged_boxes

def pdf_to_img_chunks(pdf_path):
    # Cargar el archivo PDF
    pages = convert_from_path(pdf_path, 300)
    
    image = pages[0]
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13,3))
    dilate = cv2.dilate(thresh, kernel, iterations=13)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    boxes = [cv2.boundingRect(c) for c in cnts]



    y_threshold = 10  
    grouped_boxes = merge_boxes_on_same_row(boxes, y_threshold)
    sub_images = []
    for i, (x, y, w, h) in enumerate(grouped_boxes):
        sub_image = binary[y:y+h, x:x+w]
        sub_images.append(sub_image)
    return sub_images


