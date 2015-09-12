import cv2
import numpy as np

intensity_range = 256
hue_factor = float(intensity_range)/360
flower_image_name = 'flower.jpg'

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
	return (hue, saturation, value)

def set_rgb(pixel_index, hue, saturation, value, image):
	original_hue = hue / hue_factor
	c = value * saturation / intensity_range
	x = c * (1 - abs(((original_hue / 60) % 2) - 1))
	m = value - c
	red, green, blue = m, m, m
	if original_hue < 0:
		print original_hue, 'error..............................'
	elif original_hue < 60:
		red += c
		green += x
	elif original_hue < 120:
		red += x
		green += c
	elif original_hue < 180:
		green += c
		blue += x
	elif original_hue < 240:
		green += x
		blue += c
	elif original_hue < 300:
		red += x
		blue += c
	elif original_hue < 360:
		red += c
		blue += x
	else:
		print original_hue, 'error......................'
	image[pixel_index] = [blue, green, red]

image = cv2.imread(flower_image_name, cv2.CV_LOAD_IMAGE_COLOR)
num_of_rows, num_of_cols, channels = image.shape

hue_image = np.zeros((num_of_rows,num_of_cols))
saturation_image = np.zeros((num_of_rows,num_of_cols))
value_image = np.zeros((num_of_rows,num_of_cols))
hsv2rgb = np.zeros((num_of_rows,num_of_cols, 3))

for pixel_index in np.ndindex(image.shape[:2]):
	bgr_color = image[pixel_index]
	hue, saturation, value = set_hsv(bgr_color, pixel_index, hue_image, saturation_image, value_image)
	set_rgb(pixel_index, hue, saturation, value, hsv2rgb)

cv2.imwrite('brightness.jpg', value_image)
cv2.imwrite('saturation.jpg', saturation_image)
cv2.imwrite('hue.jpg', hue_image)
cv2.imwrite('hsv2rgb.jpg', hsv2rgb)

