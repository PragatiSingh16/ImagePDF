import re
from pdfminer.high_level import extract_pages, extract_text

for page_layout in extract_pages("Java_OOPs_Concepts.pdf"):
    for element in page_layout:
        print(element)