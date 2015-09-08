import sys
import cv2
import numpy as np

original_image_name = sys.argv[1]
intensity_range = 256

image = cv2.imread(original_image_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
num_of_rows = len(image)
num_of_cols = len(image[0])
image_size = num_of_rows * num_of_cols




