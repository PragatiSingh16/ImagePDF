import os
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

img = cv2.imread('image2.jpeg')
#cv2_imshow(img)
reader = easyocr.Reader(['en'])
result = reader.readtext(img, detail = 0,paragraph="False")
result



