"""
Use: python lab2.py pic1.jpg
Note that this program might be quite slow, please be patient.
The reason is that I try to make sure the image is perfectly equalized, 
meaning the cumulative intensity graph is exactly a straight line (if the number of pixels is divisible by 256).
Also, when pixels with one original intensity can be mapped to two or more intensities after equalization, 
the new intensities will be randomly assigned by weights related to number of new intensities to be mapped to.
"""

import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_intensity_frequency(image):
	intensity_frequency = [0] * intensity_range
	for row_number in range(num_of_rows):
		for col_number in range(num_of_cols):
			intensity = image[row_number][col_number]
			intensity_frequency[intensity] += 1
	return intensity_frequency

def get_cumulative(intensity_frequency):
	cumulative = [0] * intensity_range
	cumulative[0] = intensity_frequency[0]
	for intensity in range(1, intensity_range):
		cumulative[intensity] = cumulative[intensity-1] + intensity_frequency[intensity]
	return cumulative

# Return a list of lists. If the original intensity is x,
# then for the list at new_intensity_mapper[x] :
# The first elements in each sublist are the new intensity levels mapped, 
# and second elements in each sublist represents the number of pixels 
# that will be assigned the intensity level represented by the corresponding key
def create_mapper(intensity_frequency):
	new_intensity_mapper = [[] for i in range(intensity_range)]
	original_intensity = 0
	cumulative_frequency = 0
	for new_intensity in range(1, intensity_range + 1):
		number = (new_intensity * image_size) / intensity_range
		while cumulative_frequency + intensity_frequency[original_intensity] <= number:
			new_intensity_mapper[original_intensity].append([new_intensity - 1, intensity_frequency[original_intensity]])
			cumulative_frequency += intensity_frequency[original_intensity]
			original_intensity += 1
			if (original_intensity == intensity_range):
				break
		if (original_intensity < intensity_range and cumulative_frequency < number):
			part = number - cumulative_frequency
			new_intensity_mapper[original_intensity].append([new_intensity - 1, part])
			intensity_frequency[original_intensity] -= part
			cumulative_frequency += part
	return new_intensity_mapper

def change_intensity(new_intensity_mapper):
	for row_number in range(num_of_rows):
		for col_number in range(num_of_cols):
			new_intensities = new_intensity_mapper[image[row_number][col_number]]
			weights = [i[1] for i in new_intensities]
			total = float(sum(weights))
			new_intensity = new_intensities[np.random.choice([i for i in range(len(new_intensities))], p=[i/total for i in weights])]
			image[row_number][col_number] = new_intensity[0]
			new_intensity[1] -= 1
			if (new_intensity[1] == 0):
				new_intensities.remove(new_intensity)

original_image_name = sys.argv[1]
intensity_range = 256

image = cv2.imread(original_image_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
num_of_rows = len(image)
num_of_cols = len(image[0])
image_size = num_of_rows * num_of_cols

xaxis = [i for i in range(256)]
intensity_frequency = get_intensity_frequency(image)
original_cumulative = get_cumulative(intensity_frequency)

mapper = create_mapper(intensity_frequency)
change_intensity(mapper)
image_name, extension = original_image_name.split('.')
new_image_name = image_name + '-equalized.' + extension
cv2.imwrite(new_image_name, image)

# uncomment below to plot the graphs
# final_intensity_frequency = get_intensity_frequency(image)
# plt.plot(xaxis, original_cumulative, 'r-', xaxis, get_cumulative(final_intensity_frequency), 'g-')
# plt.axis([0, intensity_range, 0, image_size])
# plt.show()