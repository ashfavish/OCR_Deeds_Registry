# OCR_Deeds_Registry
This code accompanies my dissertation which automates data capture of title deeds using Tesseract, CV2, re and other packages in python.  
The title deed pdfs are encrypted using AES encryption before being added to IPFS.

### Details of folder contents

The following files are included in the OCR package:  
1) allpreprocessing: This file has the OCR results for the simulated deeds and links to the create deed function so the csv can be generated.  
2) convertpdf: This contains function to convert pdf to a images and stores the image paths in a list for future use. This function also encrypts the pdf file and adds the encrypted file to IPFS.  
3) deskew: This function takes an image, detects any skewness and rotates image accordingly.  
4) encrypt: This file contains AES encryption and descrpytion functions using a user created password. This uses pycrypydome for encryption.  
5) fullocr: This contains the function which takes functions from the other files to create a full pipeline from pdf to data capture in a csv. 
6) imageclean: This has the function for preprocessing of images to improve performance of OCR.
7) ipfs: run this file to ensure connection to IPFS is working
8) methodology: This contains the code for the demonstrating how different parts of the pre-processing appears visually. This file was used to create the images within methodology chapter of dissertation. 
9) regex: This file has the compiled regular expressions and function used for extracting relevant data from OCR results.
10) titledeed: This file contains the classes DeedsRegsitry and TitleDeed. For the DeedsRegsitry class, there is a method to create a new registry (i.e. database/csv) if none exists. The TitleDeed class has the relevant information to be extracted as attributes. The methods within this class are create_dictionary and write_to_csv. create_dictionary takes the attributes from the object and creates the relevant number of dictionaries based on the type of deed and how many rows are recorded. write_to_csv then takes these dictionaries and writes them to a csv file.

The Simulated Deeds Scanned PDFS folder has the sample of 15 deeds which were used to test out the OCR application. The names, surname and ID numbers are randomly generated and do not reflect real people. Other information such as erf numbers and title deed numbers are simulated, but in the required format.

### Required programmes external to python required for code to work

1) Image Pre-Procesing: ImageMagick
2) OCR: Tesseract
3) IPFS

1) https://imagemagick.org/script/download.php
2) https://github.com/tesseract-ocr/tesseract/wiki/Downloads
3) https://docs.ipfs.io/introduction/install/ 


  
