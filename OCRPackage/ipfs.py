import ipfsapi

"""Will only work if connected to IPFS
1) First make sure IPFS is downloaded and works on computer
2) Go to command prompt and change to directory with ipfs
2) Start daemon to connect to IPFS and act as a node: command = ipfs daemon
More Information available at: 
https://medium.com/python-pandemonium/getting-started-with-python-and-ipfs-94d14fdffd10
"""
if __name__ == '__main__':
# Connect to local node
	try:
		api = ipfsapi.connect('127.0.0.1', 5001)
		print(api)

	except ipfsapi.exceptions.ConnectionError as ce:
		print(str(ce))
