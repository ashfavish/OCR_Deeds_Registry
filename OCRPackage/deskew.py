import numpy as np
import cv2
import matplotlib.pyplot as plt


""" Based on Adrian Rosebrock Tutorial: 
https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/"""

def deskewer(img):

	original = img
	gray = cv2.bitwise_not(img)
	thresh = cv2.threshold (gray, 0, 255,cv2.THRESH_OTSU)[1]
	coords = np.column_stack(np.where(thresh > 120))
	rotation = cv2.minAreaRect(coords)[-1]
	 
	# the `cv2.minAreaRect` function returns values in the
	# range [-90, 0); as the rectangle rotates clockwise the
	# returned angle trends to 0 -- in this special case we
	# need to add 90 degrees to the angle
	if rotation < -45:
		rotation = -(90 + rotation)
	 
	# otherwise, just take the inverse of the angle to make
	# it positive
	else:
		rotation= -rotation
	#If unexpected rotation value, ignore rotation
	if abs(rotation)>2:
		rotation=0
	print('Rotation: {:.2f} degrees'.format(rotation))
	#find shape of original image
	h,w = original.shape[:2]
	# calculate the center of the image
	center = (w / 2, h / 2)
	#Rotate image around centre 
	matrix = cv2.getRotationMatrix2D(center,rotation, 1)
	rotated = cv2.warpAffine(original, matrix, (w, h), 
		flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
	return rotated, rotation
	