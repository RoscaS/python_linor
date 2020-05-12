import numpy as np
from cv2 import cv2


def color_mask(img, low, upper):
	hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	return cv2.inRange(hsv, low, upper)

def zone_mask(img, vertices):
	# blank mask:
	mask = np.zeros_like(img)
	# fill the mask
	cv2.fillPoly(mask, vertices, 255)
	# now only show the area that is the mask
	return cv2.bitwise_and(img, mask)

def apply_canny(img, threshold1 = 200, threshold2 = 300):
	return cv2.Canny(img, threshold1, threshold2)

def apply_gaussian(img, kernel = (5,5), sigmax = 0):
	return cv2.GaussianBlur(img, kernel, sigmax)

def thiken(img, size=2, iterations=1):
	return morph(img, (size, size), iterations, mode="d")

def morpho_process(img):
	img2 = img
	# delete lines
	# img2 = morph(img2, (10, 10), mode='d')
	# img2 = morph(img2, (10,10))
	img2 = morph(img2, (3, 3), mode='d')
	img2 = morph(img2, (2,2))
	img2 = morph(img2, (2,2), mode='d')
	# strengthen intersections
	# img2 = morph(img, (9, 9), 3, mode='d')
	# img2 = morph(img2, (4, 4), 2)
	# close remaining blobs
	img2 = morph(img2, (2, 2))
	img2 = morph(img2, (2,2), mode='d')

	#
	# img2 = morph(img2, (1,1),2 )
	# img2 = morph(img2, (1,1), mode='d')


	# img2 = morph(img2, (2,2) )
	# img2 = morph(img2, (2,2),  mode='d')
	# img2 = morph(img2, (12, 12))
	# img2 = morph(img2, (3, 3))
	return img2

def morph(img, size=(3, 3), iteration=1, mode='e'):
	kernel = np.ones(size, np.uint8)
	if mode == 'e':
		return cv2.erode(img, kernel, iterations=iteration)
	else:
		return cv2.dilate(img, kernel, iterations=iteration)
