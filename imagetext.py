import pytesseract
from PIL import Image


image = Image.open("123.jpg")
text = pytesseract.image_to_string(image, lang="eng")
print(text)
