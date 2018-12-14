import ipfsapi

"""Will only work if connected to IPFS
1) First make sure IPFS is downloaded and works on computer
2) Start daemon to connect to IPFS and act as a node
More Information available at: 
https://medium.com/python-pandemonium/getting-started-with-python-and-ipfs-94d14fdffd10
"""
if __name__ == '__main__':
# Connect to local node
	try:
		api = ipfsapi.connect('127.0.0.1', 5001)
		new_file = api.add('nelson.jpg')
		print(api)
		print(new_file['Hash'])
		api.cat(new_file['Hash'])
	except ipfsapi.exceptions.ConnectionError as ce:
		print(str(ce))

	try:
		from Crypto.PublicKey import RSA
		from Crypto.Random import get_random_bytes
		from Crypto.Cipher import AES
	except ImportError:
		print("import ImportError")