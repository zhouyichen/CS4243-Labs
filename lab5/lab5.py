import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

original_image_name = sys.argv[1]
k = 0.06
image = cv2.imread(original_image_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
num_of_rows = len(image)
num_of_cols = len(image[0])

sobel_horizontal = np.array([-1, -2, -1, 0, 0, 0, 1, 2, 1])
sobel_vertical = np.array([-1, 0, 1, -2, 0, 2, -1, 0, 1])

def gauss_kernels(size, sigma=1):
	## returns a 2d gaussian kernel
	if size < 3:
		size = 3
	m = size/2
	x, y = np.mgrid[-m:m + 1, -m:m + 1]
	kernel = np.exp(-(x * x + y * y)/(2 * sigma * sigma))
	kernel_sum = kernel.sum()
	if not sum == 0:
		kernel = kernel / kernel_sum
	return kernel
gauss_kernels_3 = gauss_kernels(3)
gauss_kernels_3.resize((9, 1))

def get_adjacent_pixels(pixel_index):
	row_number, col_number = pixel_index
	mat = np.zeros((3,3))
	for i in range(3):
		row = max(0, min(row_number - 1 + i, num_of_rows - 1))
		for j in range(3):
			col = max(0, min(col_number - 1 + j, num_of_cols - 1))
			mat[i, j] = image[row, col]
	mat.resize((1, 9))
	return mat

def convolve_with_gauss(pixel_index):
	row_number, col_number = pixel_index
	W = [0, 0, 0]
	for w in range(3):
		mat = np.zeros((3,3))
		for i in range(3):
			row = max(0, min(row_number - 1 + i, num_of_rows - 1))
			for j in range(3):
				col = max(0, min(col_number - 1 + j, num_of_cols - 1))
				mat[i, j] = derivatives_mat[row, col][w]
		mat.resize((1, 9))
		W[w] = float(mat.dot(gauss_kernels_3))
	return W

derivatives_mat = np.zeros((num_of_rows, num_of_cols, 3))
response_mat = np.zeros((num_of_rows, num_of_cols))

for pixel_index in np.ndindex(image.shape[:2]):
	adjacent_pixels = get_adjacent_pixels(pixel_index)
	gx = int(adjacent_pixels.dot(sobel_vertical))
	gy = int(adjacent_pixels.dot(sobel_horizontal))
	I_xx = gx * gx
	I_xy = gx * gy
	I_yy = gy * gy
	derivatives_mat[pixel_index] = [I_xx, I_xy, I_yy]

for pixel_index in np.ndindex(image.shape[:2]):
	W_xx, W_xy, W_yy = convolve_with_gauss(pixel_index)
	W = np.matrix([[W_xx, W_xy], [W_xy, W_yy]])
	detW = np.linalg.det(W)
	traceW = W_xx + W_yy
	response = detW - k * traceW * traceW
	response_mat[pixel_index] = response

max_response = np.amax(response_mat)
treshold_response = max_response * 0.1
rows = []
cols = []
for pixel_index in np.ndindex(image.shape[:2]):
	if response_mat[pixel_index] >= treshold_response:
		rows.append(pixel_index[1])
		cols.append(pixel_index[0])

plt.figure()
plt.imshow(image, cmap='gray')
plt.hold(True)
plt.scatter(rows, cols, color='blue', alpha=0.5)
plt.show()
