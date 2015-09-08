import sys
import cv2
import numpy as np

original_image_name = sys.argv[1]
intensity_range = 256

image = cv2.imread(original_image_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
num_of_rows = len(image)
num_of_cols = len(image[0])
image_size = num_of_rows * num_of_cols

prewit_horizontal = np.array([-1, 0, 1, -1, 0, 1, -1, 0, 1])
prewit_vertical = np.array([-1, -1, -1, 0, 0, 0, 1, 1, 1])
sobel_horizontal = np.array([-1, 0, 1, -2, 0, 2, -1, 0, 1])
sobel_vertical = np.array([-1, -2, -1, 0, 0, 0, 1, 2, 1])

prewit_image = np.zeros((num_of_rows,num_of_cols))
sobel_image = np.zeros((num_of_rows,num_of_cols))
thinned_image = np.ones((num_of_rows,num_of_cols))

def get_adjacent_pixels(row_number, col_number):
	mat = np.zeros((3,3))
	for i in range(3):
		row = max(0, min(row_number - 1 + i, num_of_rows - 1))
		for j in range(3):
			col = max(0, min(col_number - 1 + j, num_of_cols - 1))
			mat[i, j] = image[row, col]
	mat.resize((1, 9))
	return mat

prewit_max = 0
prewit_min = 1000
sobel_max = 0
sobel_min = 1000

for row_number in range(num_of_rows):
	for col_number in range(num_of_cols):
		adjacent_pixels = get_adjacent_pixels(row_number, col_number)

		prewit_vertical_strength = adjacent_pixels.dot(prewit_horizontal)
		prewit_horizontal_strength = adjacent_pixels.dot(prewit_vertical)
		prewit_strength = np.sqrt(prewit_vertical_strength * prewit_vertical_strength + prewit_horizontal_strength * prewit_horizontal_strength)
		if prewit_strength > prewit_max:
			prewit_max = prewit_strength
		if prewit_strength < prewit_min:
			prewit_min = prewit_strength
		prewit_image[row_number, col_number] = prewit_strength

		sobel_vertical_strength = adjacent_pixels.dot(sobel_horizontal)
		sobel_horizontal_strength = adjacent_pixels.dot(sobel_vertical)
		sobel_strength = np.sqrt(sobel_vertical_strength * sobel_vertical_strength + sobel_horizontal_strength * sobel_horizontal_strength)
		if sobel_strength > sobel_max:
			sobel_max = sobel_strength
		if sobel_strength < sobel_min:
			sobel_min = sobel_strength
		sobel_image[row_number, col_number] = sobel_strength
		# set_prewit_and_thinned(row_number, col_number, adjacent_pixels)

for row_number in range(num_of_rows):
	for col_number in range(num_of_cols):
		prewit_image[row_number, col_number] = int(float(prewit_max - prewit_image[row_number, col_number])/(prewit_max - prewit_min) * (intensity_range - 1))
		sobel_image[row_number, col_number] = int(float(sobel_max - sobel_image[row_number, col_number])/(sobel_max - sobel_min) * (intensity_range - 1))


image_name, extension = original_image_name.split('.')
prewit_image_name = image_name + '_prewit_result.' + extension
cv2.imwrite(prewit_image_name, prewit_image)
sobel_image_name = image_name + '_sobel_result.' + extension
cv2.imwrite(sobel_image_name, sobel_image)





