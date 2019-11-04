import pytesseract as tess
tess.pytesseract.tesseract_cmd = r"C:\Users\sstella\AppData\Local\Tesseract-OCR\tesseract.exe"
from PIL import Image

image = Image.open("stef.jpg")
text = tess.image_to_string(image, lang="eng")
print(text)
