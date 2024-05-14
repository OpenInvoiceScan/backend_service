import pytesseract
from PIL import Image
import cv2

def ocr(image):
    ## Image from opencv to PIL
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    text = pytesseract.image_to_string(image)
    return text
    
