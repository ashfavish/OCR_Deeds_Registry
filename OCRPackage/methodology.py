import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
import pytesseract
from difflib import SequenceMatcher
from statistics import mean 
from deskew import deskewer
import pandas as pd

"""Binarized images"""
orig = cv2.imread("nelson.JPG",  cv2.IMREAD_GRAYSCALE)
binarized = cv2.threshold(orig,127,255,cv2.THRESH_BINARY)[1]

#Create comparison of binarized to original
plt.subplot(121)
fig = plt.imshow(orig, cmap = "gray")    
fig.axes.get_xaxis().set_visible(False)
fig.axes.get_yaxis().set_visible(False)
plt.title("Original Image")
plt.subplot(122)
fig2 =plt.imshow(binarized, cmap = "gray")
fig2.axes.get_xaxis().set_visible(False)
fig2.axes.get_yaxis().set_visible(False)
plt.title("Binarized Image")
plt.show()


"""Noisy Images"""

#Function to create noisy image from : https://stackoverflow.com/questions/22937589/how-to-add-noise-gaussian-salt-and-pepper-etc-to-image-in-python-with-opencv
def sp_noise(image,prob):
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

image = cv2.imread('Picture3.png')
imagenoise = sp_noise(image, 0.05)
kernel = np.ones((2,2),np.uint8)
opening = cv2.morphologyEx(imagenoise, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

# Show Comparison of noisy to denoised image
plt.subplot(121)
fig = plt.imshow(imagenoise)    
fig.axes.get_xaxis().set_visible(False)
fig.axes.get_yaxis().set_visible(False)
plt.title("Original Image")
plt.subplot(122)
fig2 =plt.imshow(closing)
fig2.axes.get_xaxis().set_visible(False)
fig2.axes.get_yaxis().set_visible(False)
plt.title("Noise Reduced Image")
plt.show()

textnoise = pytesseract.image_to_string(imagenoise)
print(textnoise)

textclean = pytesseract.image_to_string(closing)
print(textclean)

#See percentage similarity between actual string and OCR output
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#Create test to see results of noise reduction on OCR output
def test(repeats):
	true = "This is a noisy image which makes it more difficult to perform OCR."
	list_clean = []
	list_noisy = []

	for i in range(repeats):
		image = cv2.imread('Picture3.png')
		imagenoise = sp_noise(image, 0.05)
		kernel = np.ones((2,2),np.uint8)
		opening = cv2.morphologyEx(imagenoise, cv2.MORPH_OPEN, kernel)
		closing = cv2.morphologyEx(imagenoise, cv2.MORPH_CLOSE, kernel)
		textnoise = pytesseract.image_to_string(imagenoise)
		textclean = pytesseract.image_to_string(closing)
		clean_similarity = similar(true,textclean)
		list_clean.append(clean_similarity)
		noise_similarity = similar(true, textnoise)
		list_noisy.append(noise_similarity)
	# Find average accuracy for simulation
	meanclean = mean(list_clean)
	meannoisy = mean(list_noisy)
	return f"The similarity for the clean image is: {meanclean} and for the noisy image: {meannoisy}"	
print(test(100))


""" Deskewing Title Deed """

skew = cv2.imread("Picture6.png")
skew = cv2.cvtColor(skew, cv2.COLOR_BGR2GRAY)
#Call deskerer function from deskew.py
deskewed, angle = deskewer(skew)

#Comparison of original to deskewed
plt.subplot(121)
fig = plt.imshow(skew, cmap = "gray")    
fig.axes.get_xaxis().set_visible(False)
fig.axes.get_yaxis().set_visible(False)
plt.title("Skew Image")
plt.subplot(122)
fig2 =plt.imshow(deskewed, cmap = "gray")
plt.text(500, 45, f'Rotation: {round(angle,2)} degrees', fontsize=6)
fig2.axes.get_xaxis().set_visible(False)
fig2.axes.get_yaxis().set_visible(False)
plt.title("After Applying Deskew")
plt.show()
