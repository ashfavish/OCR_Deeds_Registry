# OCR_Deeds_Registry
This code accompanies my dissertation which automates data capture of title deeds using Tesseract, CV2, re and other packages in python.  
The title deed pdfs are encrypted using AES encryption before being added to IPFS.

The following files are included in the OCR package:  
1) allpreprocessing: This file has the OCR results for the simulated deeds and links to the create deed function so the csv can be generated.  
2) convertpdf: This contains function to convert pdf to a images and stores the image paths in a list for future use. This function also encrypts the pdf file and adds the encrypted file to IPFS.  
3) deskew: This function takes an image, detects any skewness and rotates image accordingly.  
4) encrypt: This file contains AES encryption and descrpytion functions using a user created password. This uses pycrypydome for encryption.  
5) fullocr: This contains the function which takes functions from the other files to create a full pipeline from pdf to data capture in a csv. 
6) imageclean: This has the function for preprocessing of images to improve performance of OCR.
7) 
  
