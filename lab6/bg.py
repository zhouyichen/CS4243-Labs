import cv2
import cv2.cv as cv
import numpy as np

video_file_name = 'traffic.mp4'
cap = cv2.VideoCapture(video_file_name)

frame_width = cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)
print 'width:', frame_width
frame_height = cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
print 'height:', frame_height
frame_per_second = cap.get(cv.CV_CAP_PROP_FPS)
print 'frames per second:', frame_per_second
frame_count = cap.get(cv.CV_CAP_PROP_FRAME_COUNT)
print 'frame count:', frame_count

frame_width = int(frame_width)
frame_height = int(frame_height)
frame_per_second = int(frame_per_second)
frame_count = int(frame_count)

_, img = cap.read()
avgImg = np.float32(img)
for fr in range(1, frame_count):
	_, img = cap.read()

	alpha = 1 / float(fr + 1)
	cv2.accumulateWeighted(img, avgImg, alpha)

	normImg = cv2.convertScaleAbs(avgImg) # convert into uint8 image
	cv2.imshow('img',img)
	cv2.imshow('normImg', normImg)
	print "fr = ", fr, " alpha = ", alpha

cv2.imwrite('background.jpg', normImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()