import easyocr
import cv2

reader = easyocr.Reader(['en'], gpu=True)


def ocr(image):
    ## Image from opencv to PIL
    result = reader.readtext(image, paragraph=True, 
                             text_threshold=0.3, low_text=0.3, y_ths=0.4)

    output = ''
    for (box, text) in result:
        output += text + ' '

    return output
    
