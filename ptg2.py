#!/usr/bin/env python
# -*- coding: utf-8 -*-

#TODO: filter out un- stuff [except for transuranics, of course]

import random, sqlite3, sys, string

def makelist():
	corpore = open("biglist","r")
	outfile = open("words","w")

	def scribe(code, element):
		if not element.endswith("\n"):
		  element = element + "\n"
		  
		outfile.write(code + ", " + element)
	  
	for verbum in corpore:
		scrutatum = verbum[:-2]
		legendum = verbum[:-1]
	    	
	    	#Many elements
		if scrutatum.endswith("ium"):
			scribe("$IUM_0", legendum)
		if scrutatum.endswith("ius"):
			scribe("$IUM_S", legendum[:-2] + "m")
		if scrutatum.endswith("ious"):
			scribe("$IUM_O", legendum[:-4] + "um")
		if scrutatum.endswith("eous"):
			scribe("$IUM_E", legendum[:-5] + "ium")      
		if scrutatum.endswith("ion") and not scrutatum.endswith("tion"):
			scribe("$IUM_N", legendum[:-3] + "um")
	    
		#Some elements
		if scrutatum.endswith("um") and not scrutatum.endswith("ium"):
			scribe("$XUM_0", legendum)
		if scrutatum.endswith("us"):
			if not scrutatum.endswith("ius"):
				if not scrutatum.endswith("ous"):
					scribe("$XUM_S", legendum[:-2] + "m")
		if scrutatum.endswith("ous"):
			if not scrutatum.endswith("ious") and not scrutatum.endswith("eous"):
				scribe("$XUM_O", legendum[:-4] + "um")
		if scrutatum.endswith("on"):
			if not scrutatum.endswith("ion"):
				scribe("$XUM_N", legendum[:-3] + "um")
	
		#Noble gases and some elements
		if scrutatum.endswith("on"):
			if not scrutatum.endswith("ion"):
				scribe("$XON_0", legendum)

		#Hydrogen and so on
		if scrutatum.endswith("gen"):
			scribe("$GEN_0", legendum)
		if scrutatum.endswith("gin"):
			scribe("$GEN_I", legendum[:-4] + "gen")
		if scrutatum.endswith("gine"):
			scribe("$GEN_E", legendum[:-5] + "gen")
	
		#Halogens, mostly
		if scrutatum.endswith("ine"):
			scribe("$INE_0", legendum)
		if scrutatum.endswith("ene"):
			scribe("$INE_E", legendum[:-4] + "ine")
		if scrutatum.endswith("ean"):
			scribe("$INE_A", legendum[:-4] + "ine")	
		if scrutatum.endswith("een"):
			scribe("$INE_F", legendum[:-4] + "ine")
		
		#Sulphur
		if scrutatum.endswith("ur") and not scrutatum.endswith("our") and not scrutatum.endswith("eur"):
			scribe("$FUR_0", legendum)
	
		#Manganese
		if scrutatum.endswith("ese"):
			scribe("$ESE_0", legendum)
		if scrutatum.endswith("eze"):
			scribe("$ESE_Z", legendum[:-4]+"ese")
		if scrutatum.endswith("ease"):
			scribe("$ESE_A", legendum[:-5]+"ese")
		if scrutatum.endswith("ees"):
			scribe("$ESE_E", legendum[:-4]+"ese")

		#Iron
		if scrutatum.endswith("ron"):
			scribe("$RON_0", legendum)

		#Cobalt	
		if scrutatum.endswith("alt"):
			scribe("$ALT_0", legendum)	
		if scrutatum.endswith("olt"):
			scribe("$ALT_O", legendum[:-4] + "alt")

		#Nickel
		if scrutatum.endswith("ckel"):
			scribe("$KEL_0", legendum)
		if scrutatum.endswith("kel"):
			scribe("$KEL_K", legendum)
		if scrutatum.endswith("ckle"):
			scribe("$KEL_L", legendum[:-3]+"el")
	
		#Copper
		if scrutatum.endswith("per"):
			scribe("$PER_0", legendum)
	
		#Zinc
		if scrutatum.endswith("inc"):
			scribe("$INC_0", legendum)
		if scrutatum.endswith("ink"):
			scribe("$INC_K", legendum[:-2]+"c")
	
		#Arsenic
		if scrutatum.endswith("nic"):
			scribe("$NIC_0", legendum)
		if scrutatum.endswith("nick"):
			scribe("$NIC_K", legendum[:-2])
	
		#Silver
		if scrutatum.endswith("ver"):
			scribe("$VER_0", legendum)
		
		#Tin
		if scrutatum.endswith("in"):
			scribe("$TIN_0", legendum)
		if scrutatum.endswith("inn"):
			scribe("$TIN_N", legendum[:-2])
	
		#Antimony
		if scrutatum.endswith("ony"):
			scribe("$ONY_0", legendum)
		if scrutatum.endswith("oni"):
			scribe("$ONY_I", legendum[:-2] + "y")
	
		#Gold
		if scrutatum.endswith("old"):
			scribe("$OLD_0", legendum)
	
		#Mercury
		if scrutatum.endswith("ury"):
			scribe("$URY_0", legendum)
	
		#Lead
		if scrutatum.endswith("ead"):
			scribe("$EAD_0", legendum)
		if scrutatum.endswith("ed"):
			scribe("$EAD_E", legendum[:-2]+"ad")
	
		#Bismuth
		if scrutatum.endswith("uth"):
			scribe("$UTH_0", legendum)
		
		#Tungsten
		if scrutatum.endswith("ten"):
			scribe("$TEN_0", legendum)	
	
	corpore.close()
	outfile.close()

def loaddb():
	serialindex = 1000
	elements = open("elements","r")
	wordsdb = sqlite3.connect('wordsdb')
	#unicode magic
	wordsdb.text_factory = str
	w = wordsdb.cursor()

	for line in elements:
		splitline = line.strip().split(",")
		newz = splitline[0]
		newname = splitline[1][1:]
		newending = splitline[2][1:]	
		newcode = "0"
		rating = 0
		serialindex = serialindex + 1
		t = (newz, newcode, newending, newname, rating, serialindex)
		w.execute("insert into realtable values (?, ?, ?, ?, ?, ?)", t)
		serialindex = serialindex + 1000
		t = (newz, newcode, newending, newname, rating, serialindex)
		w.execute("insert into newtable values (?, ?, ?, ?, ?, ?)", t)
		serialindex = serialindex - 1000
	elements.close()

	serialindex = 3000
	words = open("words","r")
	
	for line in words:
		splitline = line.strip().split(",")
		print(line)
		
		newname = splitline[1][1:]
		splittag = splitline[0].split("_")
		newending = splittag[0]
		newcode = splittag[1]
		rating = 0
		serialindex = serialindex + 1
		t = (newcode, newending, newname, rating, serialindex)
		w.execute("insert into wordlist values (?, ?, ?, ?, ?)", t)
	
	words.close()	
	wordsdb.commit()
	w.close()
		
def compile_db():
    makelist()
    loaddb()
    
def generatesymbol(name,override):
	letters = "abcdefghijklmnopqrstuvwxyz"
	if override:
		return name[0].upper() + random.choice(letters)
	if random.randint(1,8) == 8:
		return name[0].upper()
	else:
		return name[0].upper() + name[random.randint(1,len(name)-1)].lower()				
	
def pullname(z,params):
	realending, realname, realserial = "", "", 0
	initcheck, lencheck = "", ""
	params = (MATCHLEN,MATCHINIT,ENGLISHPLEASE)
	realprops = list([x for x in w.execute("select ending, name, serial from realtable where z = ?",(z,))][0])
	realending, realname, realserial = realprops[0], realprops[1], realprops[2] 
	if ENGLISHPLEASE:
		#Aluminium, dammit, not aluminum!
		if z == 13: realending = "$IUM"
	baulist = [realending]
	if MATCHLEN:
		lencheck = " and length(name) = ?"
		baulist = baulist + [len(realname)+1]
	if MATCHINIT:
		initcheck = " and (substr(name,1,1) = ? or substr(name,1,1) = ?)"
		baulist = baulist + [realname[0].upper(), realname[0].lower()]

	bautuple = tuple(baulist)
	
	x = w.execute("select name, serial, rating, code from wordlist"
						 " where ending = ?"
						 + lencheck
						 + initcheck
						 + " order by random()"
						 " limit 1",bautuple)
					 
	try:
		out = [list(y) for y in x][0]
		
	except IndexError:
		print("No replacement")
		return 0
	
	#Nominativise -um to -us for phosphorus
	if z == 15:
		out[0] = out[0][:-1] + "s"
	if ENGLISHPLEASE:
		#sulfur > sulphur
		if z == 16:
			out[0].replace("f","ph")
	return out

#http://bytes.com/topic/python/answers/749208-opposite-zip
def unzip(zipped):
	if len(zipped) < 1:
		raise ValueError("At least one item is required for unzip.")
	indices = range(len(zipped[0]))
	return tuple(tuple(pair[index] for pair in zipped) for index in indices)
		
def reroll(z,params):

	serialsandsymbols = list([x for x in w.execute("select serial, symbol from newtable")])
	serials, symbols = unzip(serialsandsymbols)
	oldname = [x for x in w.execute("select name from newtable where z = ?",(z,))][0][0]
	oldsymbol = [x for x in w.execute("select symbol from newtable where z = ?",(z,))][0][0]
	newname = oldname
	realelements = [x[0] for x in w.execute("select name from realtable")]
	
	if pullname(z,params):
		newname, newserial, newrating, newcode = pullname(z,params)
		if NOREALELEMENTS:
			if newname in realelements:
				print("%s is a real element!" % newname)
				return 0
		if newserial in serials:
			print("Element %s already present" % newname)
		else:
			newsymbol = generatesymbol(newname,False)
			if newsymbol in symbols:
				i = 0
				while newsymbol in symbols:
					newsymbol = generatesymbol(newname,False)
					i = i + 1
					if i > len(newname):
						newsymbol = generatesymbol(newname,True)
					print(newsymbol)
					
			print(newname)
			w.execute("update newtable set serial = ? where z = ?", (newserial, z))
			w.execute("update newtable set rating = ? where z = ?", (newrating, z))
			w.execute("update newtable set name = ? where z = ?", (newname, z))
			w.execute("update newtable set code = ? where z = ?", (newcode, z))
			w.execute("update newtable set symbol = ? where z = ?", (newsymbol, z))
	else:
		return 0

MATCHLEN = True
lencheck = ""
MATCHINIT = False
initcheck = ""
ENGLISHPLEASE = True
NOREALELEMENTS = True

params = (MATCHLEN,MATCHINIT,ENGLISHPLEASE)

#compile_db()

wordsdb = sqlite3.connect('wordsdb')
w = wordsdb.cursor()

for i in range(109):
	reroll(i+1,params)
wordsdb.commit()

templatehtml = open("template.html","r")
outhtml = open("output.html","w")
znamesymbol = list([x for x in w.execute("select z, name, symbol from newtable")])
htmldict = {}
for thing in znamesymbol:
	htmldict["S"+str(thing[0])] = thing[2]
	htmldict["E"+str(thing[0])] = thing[1].title()
	if thing[0] == 1:
		htmldict["HYDROGEN"] = thing[1].title()
	if thing[0] == 57:
		htmldict["LANTHANIDE"] = "* " + thing[1].title()[:-2]+"ide series"
	if thing[0] == 89:
		htmldict["ACTINIDE"] = "+ " + thing[1].title()[:-3]+"ide series"
		
catdic = {}
catcodes = ["$ALKALI", "$METAL", "$EARTH", "$TRANSITION", "$POOR", "$NOBLE", "$GAS", "$RARE"]
for catcode in catcodes:
	newcat = w.execute("select word from misc where code = ? order by random() limit 1", (catcode,))
	catdic[catcode] = str([x for x in newcat][0][0])
	print(catdic[catcode])

htmldict["ALKALIMETALS"] = "%s %ss" % (catdic["$ALKALI"].title(), catdic["$METAL"].lower())
htmldict["ALKALIEARTHMETALS"] = "%s %s %ss" % (catdic["$ALKALI"].title(), catdic["$EARTH"].lower(), catdic["$METAL"].lower())
htmldict["TRANSITIONMETALS"] = "%s %ss" % (catdic["$TRANSITION"].title(), catdic["$METAL"].lower())
htmldict["POORMETALS"] = "%s %ss" % (catdic["$POOR"].title(), catdic["$METAL"].lower())
htmldict["NONMETALS"] = "Non%ss" % catdic["$METAL"].lower()
htmldict["NOBLEGASES"] = "%s %ses" % (catdic["$NOBLE"].title(), catdic["$GAS"].lower())
htmldict["RAREEARTHMETALS"] = "%s %s %ss" % (catdic["$RARE"].title(), catdic["$EARTH"].lower(), catdic["$METAL"].lower())

htmldict["TABLENAME"] = "Periodic Table of the Elements"

templatelines = templatehtml.readlines()
for line in templatelines:
	outhtml.write(string.Template(line).safe_substitute(htmldict))
	
w.close()
	
	
