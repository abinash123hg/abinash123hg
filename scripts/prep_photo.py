from PIL import Image
from rembg import remove
import cv2
import numpy as np
import sys

input_file = sys.argv[1]
output_file = "source-prepped.png"

img = Image.open(input_file).convert("RGBA")
img = remove(img)

rgba = np.array(img)
alpha = rgba[:, :, 3]
gray = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2GRAY)

gray[alpha < 20] = 255

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
gray = clahe.apply(gray)

Image.fromarray(gray).save(output_file)
print(f"Saved: {output_file}")