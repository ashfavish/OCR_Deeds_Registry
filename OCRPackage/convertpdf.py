import io
from wand.image import Image as wi
from PIL import Image
import cv2
import numpy as np
import os.path

def pdf_to_image(filepath):
	# CHECK IF pdf file
	file_name, extension = os.path.splitext(filepath)
	''' Returns a list of CV2 images which are ready for further preprocessing'''
	if extension == ".pdf":
		imagelist = []
		with(wi(filename=filepath,resolution=600)) as source:
			images=source.sequence
			pages=len(images)
			for i in range(pages):
				wi(images[i]).save(filename=f"{file_name} page {i+1}.png")
				imagelist.append(f"{file_name} page {i+1}.png")
		return imagelist
	else:
		print("not pdf")
		return filepath