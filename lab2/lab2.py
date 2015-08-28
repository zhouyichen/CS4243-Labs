import sys
import cv2
import cv2.cv as cv
import numpy as np

# original_image_name = sys.argv[1]
original_image_name = 'pic1.jpg'
intensity_range = 256

image = cv2.imread(original_image_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
num_of_rows = len(image)
num_of_cols = len(image[0])
image_size = num_of_rows * num_of_cols
intensity_frequency = [0] * intensity_range

for row_number in range(num_of_rows):
	for col_number in range(num_of_cols):
		intensity = image[row_number][col_number]
		intensity_frequency[intensity] += 1

# A list of dictionaries. If the original intensity is x,
# then for the dictionary at new_intensity_mapper[x] :
# The keys are the new intensity levels mapped, 
# and the values represents the number of pixels that will be assigned the intensity level represented by the corresponding key
new_intensity_mapper = [{} for i in range(intensity_range)]
original_intensity = 0
cumulative_frequency = 0
for new_intensity in range(1, intensity_range + 1):
	number = new_intensity * image_size / intensity_range
	while cumulative_frequency + intensity_frequency[original_intensity] <= number:
		new_intensity_mapper[original_intensity][new_intensity] = intensity_frequency[original_intensity]
		cumulative_frequency += intensity_frequency[original_intensity]
		original_intensity += 1
		if (original_intensity == intensity_range):
			break
	if (original_intensity < intensity_range and cumulative_frequency < number):
		part = number - cumulative_frequency
		new_intensity_mapper[original_intensity][new_intensity] = part
		intensity_frequency[original_intensity] -= part
		cumulative_frequency += part





