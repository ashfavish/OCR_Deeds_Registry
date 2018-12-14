import re
from titledeed import DeedsRegistry, TitleDeed

#create patterns to extract releant title deed information
erfnum = re.compile(r"ERF[:]?\s(\d+.?(\s\w+)\s?(\w+[\S \t]\b)?\s*)", re.IGNORECASE)
title_num = re.compile(r"((Deed\sof\sTransfer(\s(Number\s)?(T?\d+\/\d+)))|([^.]No\.?\s(T?\d+\/\d+)))|(ST\s\d+\/\d+)", re.IGNORECASE)
buyer = re.compile(r"""on\sbe[hn]*a[li]*[ft]\sof[:.-]?\s.?\s+(\d.\s+)?(((\w+[\S \t])(\w+[\S \t]\b)?)\s(\(?(\w+[\s)])?)?\s?(\w+[\S \t]))\s+(Identity\sNumber|Registration\sNumber)[:.]?\s+(\d+.+)\s+(Married|Unmarried|an?\w?)?""", re.IGNORECASE)
seller = re.compile(r"""grante[ad]\sto\s([hn]im)*(\/?her)?\sby[:.\d\s]*((.)\1)*\s+(((((\w+[\S \t])(\w+\b[\S \t])?))(\((\w+[\s)])*)*\s?(\w+[\S \t])+)\.?\s+(Identity\sNumber|Registration\sNumber).?\s(C?K?\s?\d+.+[^(and)])\s*(Married|Unmarried)?)|(granted\sto\shim(\/her)?\sby[:]?\s+((\w+\s+)+(\((\w+[)\s])+)?)\s+(Identity\sNumber|Registration\sNumber)\s(\d+.+)\s+(Married|Unmarried)?)""",re.IGNORECASE)
regno = re.compile(r"(Registration\sNumber)\s+(\d{4}\/\d+\/\d{2})")
datesold = re.compile(r"""ha[dc]\s(truly\sand\slegally\ssol[da].?\s(t[hn]e\su\w*dermentioned\sproperty\s)?)?on\s(\d{1,2}(th)?\s(J(anuary|u(ne|ly))|February|Ma(rch|y)|A(pril|ugust)|(((Sept|Nov|Dec)em)|Octo)ber)\s\d{4})\s?(truly\sand\slegally\ssold)?""")
datetransact = re.compile(r"resolution\sdated\s(the\s)?(\d{1,2}(th\sday\sof\s)?(J(anuary|u(ne|ly))|February|Ma(rch|y)|A(pril|ugust)|(((Sept|Nov|Dec)em)|Octo)ber)\s\d{4})", re.IGNORECASE)
purchaseprice= re.compile(r"((the|an)\s(sum|amount)\sof\s(R(\d+[\s.,])+\d{2}))|(value\sof\sthe\sproperty\s(\w+\s)*(R(\d)?\s\d+\s\d+.\d{2}))")
size = re.compile(r"((\d.)?\d+)\s*\((\s?\w+[\s)]+)+\s(SQUARE\sMETRES|Hectares)", re.IGNORECASE)
datereg = re.compile(r"""(on\s.?\s?(\d{1,2}[ -]+(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s\d{4}))|(on\s+(\w?\d{3,4}.+\d{2}.+\d{2}))""")
sectionalplannum = re.compile(r"Sectional\sPlan\s(Number|No\.?)\s(SS\s\d+\/\d+)")
section_num = re.compile(r"Section\sN(o\.|umber)\s(\d+)", re.IGNORECASE)
married_icop = re.compile(r"married in community of property",re.IGNORECASE)
marriage_partner = re.compile(r"an[d\w]\s+((\w+[\S \t])(\w+[\S \t]\b)?)\s?(\w+[\S \t])\s+Identity\sNumber[:.]?\s+(\d+.+)\s+Married\sin\scommunity\sof\sproperty", re.IGNORECASE)
fractionshares = re.compile(r"a\s+(0.\d+)\s+share", re.IGNORECASE)
fractionalowner = re.compile(r"\s((\w+[\S \t])(\w+[\S \t]\b)?)\s?(\w+[\S \t])\s+Identity\sNumber[:]?\s+(\d+.+)\s+(Married(\s\w+)+|Unmarried)\s+a\s+(0.\d+)\s+share", re.IGNORECASE)
sellerRDP = re.compile(r"granted\sto\shim(\/her)?\sby[:.\d\s]*\s+((\w+[\S \t])+)", re.IGNORECASE)
RDPindicator = re.compile(r"In\sterms\sof\sthe\sprovisions\sof\sSection\s\d\sand\s\d\(\d\)\s*of\sAct\sNo.\s\d+\sof\s\d+", re.IGNORECASE)
noise = re.compile(r"\b([a-b,d-r,t-z])\1{1,}\b", re.IGNORECASE)
mortgageamount = re.compile(r"ver[a-z]+\s+mort?[a-z]\s+[F]or\s+(R\d{1-3}\s\d+\s?\d*.?\d+)", re.IGNORECASE)
"""1) Takes OCR Output as parameter
2) Extracts relevant data for extraction based on Regex
3) Creates an object of type 'Title Deed'
4) Calls on method to create row entry in CSV"""
def create_deed(list_of_strings, filehash):
	#create default values to prevent errors in running due to non-capture
	sellerfirst = " "
	sellerid = " "
	sellersurname = " "
	buyerfirst = " "
	buyerID = " "
	datetransaction = " "
	section_numbers = []
	propertysizes = []
	dateregister = " "
	price = " "
	buyerlast = " "
	sectionalplan_num = " "
	erfno = " "
	title =" "
	titleslist = [" "]
	share = "100%"
	bondamount = "0"

	for item in list_of_strings:
		#remove strange characters from OCR
		page = re.sub("[=�*;%$#@!~<>|`']", '', item)
		page =re.sub(noise, " ", page)
		#Either free-hold or sectional title
		result = re.search(erfnum, page)
		sectional = re.search(section_num, page)
		if result:
			match= erfnum.finditer(page)
			for m in match:
				# takes out text from regex match
				erfno = m.group(1)
				section_numbers = " "
		else:
			if sectional:			
				secctplannum= sectionalplannum.finditer(page)
				sectionnum= section_num.finditer(page)
				for i in secctplannum:
					sectionalplan_num = i.group(2)
				for i in sectionnum:
					section_number =i.group(2)
					section_numbers.append(section_number)

		title_numbers = title_num.finditer(page)
		for i in title_numbers:
			if i.group(5):
				title = i.group(5)
				if title[0]!="T":
					title = "T" +title[1:]
			elif i.group(7):
				title = i.group(7)
				if title[0]!="T":
					title = "T" +title[1:]
			elif i.group(8):
				title = i.group(8)
			titleslist.append(title)
		try:
			if len(titleslist)==1:
				title = " "
			elif titleslist[1][-4:]<titleslist[2][-4:]:
				title = titleslist[2]
			else:
				title = titleslist[1] 
		except IndexError: 
			pass
		# Different structure for fractional ownership
		# Search document for properties of fractional ownership
		fractionalownership = re.search(fractionshares,page)
		if fractionalownership:
			fracowners = fractionalowner.finditer(page)	
			buyerfirst = []
			buyerlast = []
			buyerID = []
			shareown = []			
			for m in fracowners:
				buyerfirst.append(m.group(1))
				buyerlast.append(m.group(4))
				buyerID.append(m.group(5))
				shareown.append(m.group(8))
			share = shareown
		else:
			buyer_prop = buyer.finditer(page)
			icop = re.search(married_icop, page)
			for m in buyer_prop:
				buyerID = m.group(10)
				married = m.group(11)
				#If not company - seperate first and last
				if m.group(0).find("LIMITED")== -1:
					#see if married in community of property
					if icop:
						buyerfirst = []
						buyerlast = []
						buyerID = []
						buyerfirst.append(m.group(3))
						buyerlast.append(m.group(8))
						buyerID.append(m.group(10))
						married_to = marriage_partner.finditer(page)
						#add details for marriage partner
						for m in married_to:
							buyerfirst.append(m.group(1))
							buyerlast.append(m.group(4))
							buyerID.append(m.group(5))
					# Else just 1 person		
					else:
						buyerfirst =m.group(3)
						buyerlast = m.group(8)
						married = m.group(11)
				else:
					#Buyer is company
					buyerfirst = m.group(2)

		#check if RDP/subsidized housing - from government
		RDP = re.search(RDPindicator, page)
		if RDP:
			sellersubsidized = sellerRDP.finditer(page)
			for i in sellersubsidized:
				sellerfirst = i.group(2)
		else:
		#Check if seller is company or person										
			sellerinfo = seller.finditer(page)
			for i in sellerinfo:
				if i.group(5):
					sellerid = i.group(15)
					if i.group(0).find("LIMITED") == -1 and i.group(0).find("LTD") == -1 and i.group(0).find("CC")==-1:
						sellerfirst = i.group(7)
						sellersurname = i.group(13)
						married = i.group(16)
					else:
						sellerfirst = i.group(6)
				elif i.group(17):
					sellerid = i.group(24)
					#seller is company
					sellerfirst = i.group(19)
				else:
					sellerfirst = " "

		#Date sold/ transaction
		sold = datesold.finditer(page)
		for i in sold:
			if i.group(3):
				datetransaction =i.group(3)
		#Check for date of transaction other than sale of property
		othertransaction = re.search(datetransact,page)
		if othertransaction:
			transaction = datetransact.finditer(page)				
			for m in transaction:
						datetransaction = m.group(2)
						datetransaction =re.sub(r"(th\s)|(day\s)|(of)","", datetransaction)
		#Find Purchase Price
		price1 = purchaseprice.finditer(page)
		for i in price1:
			if i.group(4):
				price =i.group(4)
			elif i.group(8):
				price =i.group(8)
		#Find size of property
		squaremetres = size.finditer(page)
		for i in squaremetres:
			if i.group(0):
				sizeprop =i.group(1)
				propertysizes.append(sizeprop)
			else:
				propertysizes= [" "]
			
		dateregistered= datereg.finditer(page)
		for i in dateregistered:
			if i.group(2):
				dateregister =i.group(2)
			elif i.group(5):
				dateregister =i.group(5)
		mortgage = mortgageamount.finditer(page)
		for i in mortgage:
			if i.group(0):
				bondamount =i.group(1)

	if len(section_numbers)	> len(propertysizes):
		propertysizes.append(" ")
		if len(section_numbers)	> len(propertysizes):
			propertysizes.append(" ")		
	#Create object of class Title Deed		
	deed = TitleDeed(buyerfirst, sellerfirst, buyerID, sellerid, propertysizes, datetransaction, 
		dateregister, price, title, buyerlast, sellersurname, erfno,sectionalplan_num, section_numbers,
		bondamount, share, filehash)
	#Create dictionary of inputs
	deed.create_dictionary()
	#Write dictionary to CSV
	deed.write_to_csv()





