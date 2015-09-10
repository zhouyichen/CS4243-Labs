import cv2
import numpy as np

intensity_range = 256
hue_factor = float(intensity_range)/360
original_image_name = 'flower.jpg'

def set_hsv(bgr_color, pixel_index, hue_image, saturation_image, value_image):
	b, g, r = bgr_color.astype(int)

	cmax = max(r, g, b)
	cmin = min(r, g, b)
	delta = cmax - cmin

	value = cmax
	value_image[pixel_index] = value

	if cmax == 0:
		saturation = 0
	else:
		saturation = intensity_range * delta / cmax
	saturation_image[pixel_index] = saturation

	if delta < 1:
		hue = 0
	elif cmax == r:
		hue = 60 * ((float(g - b) / delta) % 6)
	elif cmax == g:
		hue = 60 * (float(b - r) / delta + 2)
	else:
		hue = 60 * (float(r - g) / delta + 4)
	hue = int(hue * hue_factor)

	hue_image[pixel_index] = hue

image = cv2.imread(original_image_name, cv2.CV_LOAD_IMAGE_COLOR)
num_of_rows, num_of_cols, channels = image.shape

hue_image = np.zeros((num_of_rows,num_of_cols))
saturation_image = np.zeros((num_of_rows,num_of_cols))
value_image = np.zeros((num_of_rows,num_of_cols))

for pixel_index in np.ndindex(image.shape[:2]):
	bgr_color = image[pixel_index]
	hsv = set_hsv(bgr_color, pixel_index, hue_image, saturation_image, value_image)

image_name, extension = original_image_name.split('.')
value_image_name = 'brightness.' + extension
cv2.imwrite(value_image_name, value_image)
saturation_image_name = 'saturation.' + extension
cv2.imwrite(saturation_image_name, saturation_image)
hue_image_name = 'hue.' + extension
cv2.imwrite(hue_image_name, hue_image)