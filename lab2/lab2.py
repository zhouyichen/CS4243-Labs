import sys
import cv2
import cv2.cv as cv
import numpy as np

# original_image_name = sys.argv[1]
original_image_name = 'pic1.jpg'

image = cv2.imread(original_image_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)

intensity_frequency = [0] * 256

for row in image:
	for pixel in row:
		intensity_frequency[pixel] += 1

print(intensity_frequency)
