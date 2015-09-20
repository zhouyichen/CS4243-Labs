import cv2
import numpy as np
import matplotlib.pyplot as plt

intensity_range = 256

def gauss_kernels(size,sigma=1):
	## returns a 2d gaussian kernel
	if size < 3:
		size = 3
	m = size / 2
	x, y = np.mgrid[-m:m + 1, -m:m + 1]
	kernel = np.exp(-(x * x + y * y)/(2 * sigma * sigma))
	kernel_sum = kernel.sum()
	if not sum == 0:
		kernel = kernel / kernel_sum
	return kernel
