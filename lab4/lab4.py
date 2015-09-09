import cv2
import numpy as np

intensity_range = 256
hue_factor = float(intensity_range)/360

def set_hsv(bgr_color, pixel_index, hue_image, saturation_image, value_image):
	blue, green, red = bgr_color
	r = red/255
	g = green/255
	b = blue/255
	cmax = max(r, g, b)
	cmin = min(r, g, b)
	delta = cmax - cmin
	if (delta < 1):
		hue = 0
	elif cmax == r:
		hue = 60 * ((float(g-b) / delta) % 6)
	elif cmax == g:
		hue = 60 * (float(b-r) / delta + 2)
	else:
		hue = 60 * (float(r-g) / delta + 4)
	hue = int(hue * hue_factor)


image = cv2.imread('flower.jpg', cv2.CV_LOAD_IMAGE_COLOR)
num_of_rows, num_of_cols, channels = image.shape

hue_image = np.zeros((num_of_rows,num_of_cols))
saturation_image = np.zeros((num_of_rows,num_of_cols))
value_image = np.zeros((num_of_rows,num_of_cols))


for pixel_index in np.ndindex(image.shape[:2]):
	bgr_color = image[pixel_index]
	print bgr_color, pixel_index
	hsv = set_hsv(bgr_color, pixel_index, hue_image, saturation_image, value_image)

for i in range(256):
	hsv = np.uint8([[[i, 255, 255]]])
	bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
	print i, bgr
