import sys
import cv2
import cv2.cv as cv
import numpy as np
import matplotlib.pyplot as plt

# original_image_name = sys.argv[1]
original_image_name = 'pic5.jpg'
intensity_range = 256

image = cv2.imread(original_image_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
num_of_rows = len(image)
num_of_cols = len(image[0])
image_size = num_of_rows * num_of_cols

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

# A list of dictionaries. If the original intensity is x,
# then for the dictionary at new_intensity_mapper[x] :
# The keys are the new intensity levels mapped, 
# and the values represents the number of pixels that will be assigned the intensity level represented by the corresponding key
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


xaxis = [i for i in range(256)]
intensity_frequency = get_intensity_frequency(image)
mapper = create_mapper(intensity_frequency)
change_intensity(mapper)
# intensity_frequency = get_intensity_frequency(image)

# plt.plot(get_cumulative(intensity_frequency))
# plt.axis([0, intensity_range, 0, image_size])
# plt.show()

image_name, extension = original_image_name.split('.')
new_image_name = image_name + '-equalized.' + extension
cv2.imwrite(new_image_name, image)


