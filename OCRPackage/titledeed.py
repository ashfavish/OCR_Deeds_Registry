import csv

class DeedsRegistry():
	"""DeedsRegistry - Registry Branch
	Based in a certain city"""
	def __init__(self, city):
		self.branch = city
		#self.titledeeds_registered = {}

	#Creates new registry if none exists
	def create_registry(self):
		try:
			with open(f'titledeeds.csv', 'w') as csvfile:
				writer = csv.DictWriter(csvfile,fieldnames = ['buyerfirstname', 'buyersurname', 'buyerID', 
				'sellerfirstname', 'sellersurname', 'sellerID', 'erfno', 'title_num', 'size' ,' datetransaction',
				 'dateregistration' ,'sectionplan_num', 'section_number','price','bondamount', 'share', 'filehash'])
				writer.writeheader()
		except Exception as e:
			raise e
		else:
			print("file exists")


class TitleDeed():
	"""TitleDeed Class
	Stores the required information to be captured into deeds database"""
	def __init__(self, buyerfirstname, sellerfirstname, buyerID, sellerID, size,
		datetransaction, dateregistration, price,title_num = " ",buyersurname = " ",sellersurname = " ",
		 erfno = " ", sectionplan_num = " ",section_number = " ",bondamount = 0, share = "100%", filehash = " "):
		self.buyerfirstname = buyerfirstname
		self.buyersurname = buyersurname
		self.buyerID = buyerID
		self.sellerfirstname = sellerfirstname
		self.sellersurname = sellersurname
		self.sellerID = sellerID
		self.erfno = erfno
		self.title_num = title_num
		self.size = size
		self.price = price
		self.datetransaction = datetransaction
		self.dateregistration = dateregistration
		self.sectionplan_num = sectionplan_num
		self.section_number = section_number
		self.bondamount = bondamount
		self.share = share
		self.dictionary = []
		self.filehash = filehash

	""" Creates a dictionary of the data to be captured in 
	CSV based on title deed contents"""
	def create_dictionary(self):
		i = 0
		if isinstance(self.buyerfirstname, list):
			#fractional ownership/married ICOP and sectional title
			if len(self.section_number) > 1:
				for section in range(len(self.section_number)):
					for buyers in range(len(self.buyerfirstname)):
						self.dictionary.append({"buyerfirstname": self.buyerfirstname[buyers],"buyersurname" : self.buyersurname[buyers] ,
						 "buyerID":self.buyerID[buyers],"sellerfirstname":self.sellerfirstname, "sellersurname":self.sellersurname, 
						 "sellerID": self.sellerID, "erfno": self.erfno,"title_num": self.title_num, "size":self.size[section], 
						 "datetransaction" : self.datetransaction, 
						 "dateregistration" : self.dateregistration, "sectionplan_num" : self.sectionplan_num,
						 "section_number" : self.section_number[section],'price' : self.price,"bondamount": self.bondamount, 
						 "share":self.share[buyers], 'filehash' : self.filehash})
			else:
				#Fractional ownership  - % share ownership is in list form
				if isinstance(self.share, list):
					for buyers in range(len(self.buyerfirstname)):
						self.dictionary.append({"buyerfirstname": self.buyerfirstname[buyers],"buyersurname" : self.buyersurname[buyers] ,
						 "buyerID":self.buyerID[buyers],"sellerfirstname":self.sellerfirstname, "sellersurname":self.sellersurname, 
						 "sellerID": self.sellerID, "erfno": self.erfno,"title_num": self.title_num, "size":self.size[0], 
						 "datetransaction" : self.datetransaction,  "dateregistration" : self.dateregistration,
						  "sectionplan_num" : self.sectionplan_num, "section_number" : self.section_number,'price' : self.price,
						  "bondamount": self.bondamount, "share":self.share[buyers], 'filehash' : self.filehash})
				else:
					#Married ICOP
					for buyers in range(len(self.buyerfirstname)):
						self.dictionary.append({"buyerfirstname": self.buyerfirstname[buyers],"buyersurname" : self.buyersurname[buyers] ,
						 "buyerID":self.buyerID[buyers],"sellerfirstname":self.sellerfirstname, "sellersurname":self.sellersurname, 
						 "sellerID": self.sellerID, "erfno": self.erfno,"title_num": self.title_num, "size":self.size[0], 
						 "datetransaction" : self.datetransaction,  "dateregistration" : self.dateregistration,
						  "sectionplan_num" : self.sectionplan_num, "section_number" : self.section_number,'price' : self.price,
						  "bondamount": self.bondamount, "share":self.share, 'filehash' : self.filehash})

		if len(self.section_number) > 1:
			#if multiple section numbers,need to create multiple rows
			# For Sectional Title Properties
			for section in range(len(self.section_number)):
				self.dictionary.append({"buyerfirstname": self.buyerfirstname,"buyersurname" : self.buyersurname ,
				 "buyerID":self.buyerID,"sellerfirstname":self.sellerfirstname, "sellersurname":self.sellersurname, 
				 "sellerID": self.sellerID, "erfno": self.erfno,"title_num": self.title_num, "size":self.size[section], 
				 "datetransaction" : self.datetransaction, 
				 "dateregistration" : self.dateregistration, "sectionplan_num" : self.sectionplan_num,
				 "section_number" : self.section_number[section],'price' : self.price,"bondamount": self.bondamount,
				 "share":self.share, 'filehash' : self.filehash})
		#For Standard Title deed
		elif len(self.section_number)==1:
			self.dictionary.append({"buyerfirstname": self.buyerfirstname,"buyersurname" : self.buyersurname ,
				 "buyerID":self.buyerID,"sellerfirstname":self.sellerfirstname, "sellersurname":self.sellersurname, 
				 "sellerID": self.sellerID, "erfno": self.erfno,"title_num": self.title_num,"size":self.size[0], "datetransaction" : self.datetransaction, 
				 "dateregistration" : self.dateregistration, "sectionplan_num" : self.sectionplan_num,
				 "section_number" : self.section_number,'price' : self.price,"bondamount": self.bondamount,
				 "share":self.share, 'filehash' : self.filehash})
		else:
			self.dictionary.append({"buyerfirstname": self.buyerfirstname,"buyersurname" : self.buyersurname ,
				 "buyerID":self.buyerID,"sellerfirstname":self.sellerfirstname, "sellersurname":self.sellersurname, 
				 "sellerID": self.sellerID, "erfno": self.erfno,"title_num": self.title_num,"size":self.size[0], "datetransaction" : self.datetransaction, 
				 "dateregistration" : self.dateregistration, "sectionplan_num" : self.sectionplan_num,
				 "section_number" : self.section_number,'price' : self.price,"bondamount": self.bondamount,
				 "share":self.share, 'filehash' : self.filehash})

	def write_to_csv(self):
	#Write dictionary of each title deed to a CSV
		with open('titledeeds.csv', 'a',  newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = ['buyerfirstname', 'buyersurname', 'buyerID', 
				'sellerfirstname', 'sellersurname', 'sellerID', 'erfno','title_num', 'size' ,'datetransaction', 'dateregistration' ,
				'sectionplan_num', 'section_number','price','bondamount', 'share', 'filehash'])
			#writer.writeheader()
			writer.writerows(self.dictionary)

ctregistry = DeedsRegistry("Cape Town")
ctregistry.create_registry()

