#Import relevant packages
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageFilter
from PIL import Image 
from deskew import deskewer
from imageclean import clean_image
from convertpdf import pdf_to_image
import os
import pytesseract
from regex import create_deed
from pathlib import Path
import re

"""Function takes a pdf of a scanned title deed
1) Converts pdf to images
2) Pre-Processes images by binarization, rescaling,
 removing noise, deskewing and making image greyscale
3) Apply tesseract OCR and convert images to strings and characters
4) Clean up text by removing strange symbols and obvious unremoved noise
5) Append cleaned text to a list
6) Use regular expressions and Title Deeds Class to create entry in CSV 
of deeds registry data"""
def ocr_pdf(pdf, noisereduce = True, deskew = True):
	cv2list, filehash = pdf_to_image(pdf)
	print(len(cv2list))
	print(cv2list)
	print(filehash)
	proc_img_list = []
	i = 1
	textlist = []
	#takes in list of cv2 images and processes each picture
	for img in cv2list:
		processed_image = clean_image(img, binarization = "simple", enhance = noisereduce, skew = deskew)
		proc_img_list.append(processed_image)
		#remove image files
		os.remove(img)
	for proc_img in  proc_img_list:
		text = pytesseract.image_to_string(proc_img,lang = "eng")
		text = text.encode('ascii', 'ignore').decode("utf-8")
		#remove strange characters from OCR
		text = re.sub("[=�*;%$#@!~<>|`']", '', text)
		textlist.append(text)

	print(textlist)
	create_deed(textlist,filehash)
	return textlist

# Applying Full OCR to Simulated Deeds

# frac1 = ocr_pdf("FracOwn1M.pdf")
#frac2 = ocr_pdf("FracOwn2.pdf")
#frac3 = ocr_pdf("FracOwn3.pdf")
#icop1 = ocr_pdf("ICOP1.pdf")
#icop2 = ocr_pdf("ICOP2.pdf")
# norm1 = ocr_pdf("Norm1.pdf",True, True )
# norm2 = ocr_pdf("Norm2M.pdf",True, True)
# norm3 = ocr_pdf("Norm3.pdf",True, True)
# rdp1 = ocr_pdf("RDP1.pdf", True,True)
# rdp2 = ocr_pdf("RDP2.pdf", True,True)
# rdp3 = ocr_pdf("RDP3.pdf", True,True)
# sect1=ocr_pdf("Sect1.pdf", True,True)
# sect2=ocr_pdf("Sect2.pdf", True,True)
# sect3=ocr_pdf("Sect3M.pdf", True,True)
# sect4=ocr_pdf("Sect4.pdf", True,True)
