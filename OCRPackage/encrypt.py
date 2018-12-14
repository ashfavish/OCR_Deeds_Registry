"""Encryption and Decryption functions based
 on watching video tutorial by DrapsTV
 https://www.youtube.com/watch?v=lSrrhP2vFS8"""

import os
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome import Random
import ipfsapi

"""function to encrypt a file which takes a key (a password
which has been hashed) and the file name"""
def encrypt(key, filename):
    #size of chunks to be encrypted
    chunksize = 64*1024
    outputfile= f"encryped{filename}"
    #make sure all sized are 16 bits
    filesize = str(os.path.getsize(filename)).zfill(16)
    #The Initialization vector
    IV = Random.new().read(16)
    #AES (acronym of Advanced Encryption Standard) is a symmetric encryption algorithm
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    
    with open(filename, "rb") as infile:
        with open(outputfile, "wb") as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)
            
            while True:
                chunk = infile.read(chunksize)
                if len(chunk)==0:
                    break
                elif len(chunk)%16 != 0:
                    #adds padding to chunk
                    chunk += b" "*(16-(len(chunk)%16))
                    #encrypts each chunk of file
                outfile.write(encryptor.encrypt(chunk))
    return outputfile
        
def decrypt(key, filename):
    chunksize = 64*1024
    outputfile = f"2.{filename[8:]}"
    with open(filename, "rb") as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)
        
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        with open(outputfile, "wb") as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk)==0:
                        break
                    outfile.write(decryptor.decrypt(chunk)) 
                outfile.truncate(filesize)
    return outputfile
                
def getKey(password):
    hasher = SHA256.new(password.encode("utf-8"))
    return hasher.digest()

#Test encryption of image
def main():
    password = getKey("password")
    encrypted = encrypt(password, "009.jpg")
    decrypted = decrypt(getKey("abc123"),"Qma2bA7dREcfhtNcSXaFFxhgGtdrnqRaa3qKsCLhTdaY62")
    #Try add encrypted file to IPFS   
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
        encryp = api.add(encrypted)
        original = api.add("009.jpg")
        decryp = api.add(decrypted)
        print(api)
        print(encryp['Hash'])
        print(original['Hash'])
        print(decryp['Hash'])
    except ipfsapi.exceptions.ConnectionError as ce:
        print(str(ce))
    #Remove files
    #os.remove(decrypted) 
    #os.remove(encrypted)

if __name__ == '__main__':
    main()