# OCR_Deeds_Registry
This code accompanies my dissertation which automates data capture of title deeds using Tesseract, CV2, re and other packages in python.  
The title deed pdfs are encrypted using AES encryption before being added to IPFS.

### Details of folder contents

The following files are included in the OCR package: 

1) allpreprocessing: This file has the OCR results for the simulated deeds and links to the create deed function, so the csv can be generated.
2) convertpdf: This contains function to convert pdf to images and stores the image paths in a list for future use. This function also encrypts the pdf file (using functions from encrypt file) and adds the encrypted file to IPFS. If IPFS dameon is not running, the conversion to images will continue and a message will print indicating that IPFS part of function could not be completed and file hash will be an empty string. The function takes the file path to a pdf. If the file is a pdf, the function will return the list of image paths and the file hash for the encrypted pdf. If the file is not a pdf, the function will return the file path and the file hash. 
3) deskew: This function takes an image, detects any skewness and rotates image accordingly.
4) encrypt: This file contains AES encryption and decryption functions using a user created password. This uses pycryptodome for encryption and decryption. 
5) fullocr: This contains the function which takes functions from the other files to create a full pipeline from pdf to data capture in a csv. The input parameters are the pdf file path and possible parameters to adjust text cleaning process. This function then calls the function from convertpdf to convert pdf to images, encrypt pdf and upload encrypted pdf to IPFS. The images are then pre-processed before OCR by calling the clean_image function from imageclean. OCR using pytesseract is performed with the text output appended to a list for each output page. The text output then goes through the create_deed function from regex which extracts the relevant data using regular expressions and writes it to a csv file. 
6) imageclean: This has the function for pre-processing of images to improve performance of OCR. The pre-processing function contains binarization, rescaling, removing noise, deskewing and converting image to greyscale. This function takes an image path as a parameter.
7) ipfs: run this file to ensure connection to IPFS is working. This should be done before using the fullocr package or else files will not be uploaded to IPFS. This is a tester file and doesn’t link to any other file. 
8) methodology: This contains the code for the demonstrating how different parts of the pre-processing appears visually. This file was used to create the images within methodology chapter of dissertation.
9)regex: This file has the compiled regular expressions and function used for extracting relevant data from OCR results and cleaning OCR results for noisy characters.
10) titledeed: This file contains the classes DeedsRegsitry and TitleDeed. For the DeedsRegsitry class, there is a method to create a new registry (i.e. database/csv) if none exists. The TitleDeed class stores the relevant data extracted as attributes. The methods within this class are create_dictionary and write_to_csv. create_dictionary takes the attributes from the object and creates the relevant number of dictionaries based on the type of deed and how many rows need to be recorded. write_to_csv then takes these dictionaries and writes them to a csv file where each dictionary represents one row of the csv.


The Simulated Deeds Scanned PDFS folder has the sample of 15 deeds which were used to test out the OCR application. The names, surname and ID numbers are randomly generated and do not reflect real people. Other information such as erf numbers and title deed numbers are simulated, but in the required format.

### Required programmes external to python required for code to work

1) Image Pre-Procesing: ImageMagick
2) OCR: Tesseract
3) IPFS

These programmes are available for download at the following links:

1) https://imagemagick.org/script/download.php
2) https://github.com/tesseract-ocr/tesseract/wiki/Downloads
3) https://docs.ipfs.io/introduction/install/ 


  
