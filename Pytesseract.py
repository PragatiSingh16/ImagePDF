from PIL import Image
from pytesseract import pytesseract
import enum
import os

os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

class OS(enum.Enum):
    Mac = 0
    Windows = 1

class ImageReader:
    def __init__ (self, os: OS):
        if os == OS.Mac:
            print('Running on: MAC\n')
        if os == OS.Windows:
            windows_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            pytesseract.tesseract_cmd = windows_path
            print('Running on: Window\n')

    def extract_text(self, image: str, lang: str) -> str:
        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img)
        return extracted_text

if __name__ == '__main__':
    ir = ImageReader(OS.Windows)
    text = ir.extract_text('image5.jpeg',lang='eng')
    pro_text = ' '.join(text.split())
    print(pro_text)