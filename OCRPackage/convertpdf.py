import io
from wand.image import Image as wi
from PIL import Image
import cv2
import numpy as np
import os.path
import ipfsapi
from encrypt import getKey, encrypt, decrypt

def pdf_to_image(filepath):
	#encrypt file to be uploaded onto IPFS 
	encrypted = encrypt(getKey("abc123"), filepath)
	#try connect to IPFS
	try:
		api = ipfsapi.connect('127.0.0.1', 5001)
		new_file = api.add(encrypted)
		filehash = new_file['Hash']
	except ipfsapi.exceptions.ConnectionError as ce:
		print("Check if Dameon is switched on")
		filehash = " "
	os.remove(encrypted)
	# CHECK IF pdf file
	file_name, extension = os.path.splitext(filepath)
	''' Returns a list of CV2 images which are ready for further preprocessing'''
	#See if in pdf form - otherwise return image path
	if extension == ".pdf":
		imagelist = []
		with(wi(filename=filepath,resolution=400)) as source:
			images=source.sequence
			pages=len(images)
			for i in range(pages):
				wi(images[i]).save(filename=f"{file_name} page {i+1}.png")
				imagelist.append(f"{file_name} page {i+1}.png")
		return imagelist, filehash
	else:
		print("not pdf")
		return filepath, filehash