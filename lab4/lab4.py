import cv2
import numpy as np

intensity_range = 256
hue_factor = float(intensity_range)/360

def convert_hsv(bgr_color, hue_image, saturation_image, value_image):
	b, g, r = bgr_color.astype(int)
	cmax = max(r, g, b)
	cmin = min(r, g, b)
	delta = cmax - cmin
	value = cmax / float(intensity_range - 1)
	if cmax == 0:
		saturation = 0
	else:
		saturation = float(delta) / cmax
	if delta < 1:
		hue = 0
	elif cmax == r:
		hue = 60 * ((float(g - b) / delta) % 6)
	elif cmax == g:
		hue = 60 * (float(b - r) / delta + 2)
	else:
		hue = 60 * (float(r - g) / delta + 4)
	return (hue, saturation, value)

def set_rgb(pixel_index, hue, saturation, value, image):
	c = value * saturation
	x = c * (1 - abs(((hue / 60) % 2) - 1))
	m = value - c
	red, green, blue = m, m, m
	if hue < 0:
		print hue, 'error..............................'
	elif hue < 60:
		red += c
		green += x
	elif hue < 120:
		red += x
		green += c
	elif hue < 180:
		green += c
		blue += x
	elif hue < 240:
		green += x
		blue += c
	elif hue < 300:
		red += x
		blue += c
	elif hue < 360:
		red += c
		blue += x
	else:
		print hue, 'error......................'
	image[pixel_index] = [int(blue * 255), int(green * 255), int(red * 255)]

def equalise(value_channel):
	hist, bins = np.histogram(value_channel.flatten(), 256, [0, 256])
	cdf = hist.cumsum()
	cdf_m = np.ma.masked_equal(cdf, 0)
	cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
	cdf = np.ma.filled(cdf_m, 0).astype('uint8')
	return cdf[value_channel.astype('uint8')]

flower_image_name = 'flower.jpg'
image = cv2.imread(flower_image_name, cv2.CV_LOAD_IMAGE_COLOR)
num_of_rows, num_of_cols, channels = image.shape

hue_image = np.zeros((num_of_rows,num_of_cols))
saturation_image = np.zeros((num_of_rows,num_of_cols))
value_image = np.zeros((num_of_rows,num_of_cols))
hsv2rgb = np.zeros((num_of_rows,num_of_cols, 3))

for pixel_index in np.ndindex(image.shape[:2]):
	bgr_color = image[pixel_index]
	hue, saturation, value = convert_hsv(bgr_color, hue_image, saturation_image, value_image)
	# normalise
	normalised_hue = int(hue * hue_factor)
	normalised_saturation = int((intensity_range - 1) * saturation)
	normalised_value = int((intensity_range - 1) * value)
	# save values into images
	hue_image[pixel_index] = normalised_hue
	saturation_image[pixel_index] = normalised_saturation
	value_image[pixel_index] = normalised_value
	set_rgb(pixel_index, hue, saturation, value, hsv2rgb)

cv2.imwrite('brightness.jpg', value_image)
cv2.imwrite('saturation.jpg', saturation_image)
cv2.imwrite('hue.jpg', hue_image)
cv2.imwrite('hsv2rgb.jpg', hsv2rgb)

bee_image_name = 'bee.png'
image = cv2.imread(bee_image_name, cv2.CV_LOAD_IMAGE_COLOR)
num_of_rows, num_of_cols, channels = image.shape

hue_image = np.zeros((num_of_rows,num_of_cols))
saturation_image = np.zeros((num_of_rows,num_of_cols))
value_image = np.zeros((num_of_rows,num_of_cols))
hsv2rgb = np.zeros((num_of_rows,num_of_cols, 3))

for pixel_index in np.ndindex(image.shape[:2]):
	bgr_color = image[pixel_index]
	hue, saturation, value = convert_hsv(bgr_color, hue_image, saturation_image, value_image)
	# normalise
	normalised_value = int((intensity_range - 1) * value)
	# save values into images
	hue_image[pixel_index] = hue
	saturation_image[pixel_index] = saturation
	value_image[pixel_index] = normalised_value

value_image = equalise(value_image)
make_float = np.vectorize(lambda value: value / float(intensity_range - 1))
value_image = make_float(value_image)

for pixel_index in np.ndindex(image.shape[:2]):
	set_rgb(pixel_index, hue_image[pixel_index], saturation_image[pixel_index], value_image[pixel_index], hsv2rgb)

cv2.imwrite('histeq.jpg', hsv2rgb)