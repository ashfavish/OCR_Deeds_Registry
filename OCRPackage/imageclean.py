#Importing Packages
import cv2
import numpy as np
from deskew import deskewer

"""Function for pre-processing the TItle Deed Scans"""
def clean_image(imagepath, greyscale = True, rescaling = True,  enhance = True, blur = True, 
    binarization = "simple", skew = True):
    #read in image
    image = cv2.imread(imagepath)
    #convert to greyscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Resize images for better results
    if rescaling == True:
        image = cv2.resize(image, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)    
    #Deskew image using deskewer function
    if skew == True:
        image, angle  = deskewer(image)
    #Choose binarization method
    if binarization == "otsu":
        image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    elif binarization == "adaptive":
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)[1]
    elif binarization == "simple":
        image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)[1]
    #Noise Removal
    if enhance == True:
        kernel = np.ones((1,1), np.uint8)
        image= cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        image= cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    if blur == True:
        image = cv2.bilateralFilter(image,9,75,75)
    return image




