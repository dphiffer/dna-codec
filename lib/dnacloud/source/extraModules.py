# -*- coding: utf-8 -*-
"""
#########################################################################
Author: Shalin Shah
Project: DNA Cloud
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Date: 5 November 2013
Website: www.guptalab.org/dnacloud
This module contains all the required and necessary methods used else where in the code.
#########################################################################
"""

from cStringIO import StringIO
import sqlite3
import math
import sqlite3 as lite
import unicodedata
import time
import csv
import sys
import HuffmanDictionary
#import wx
#import psutil
import thread
import os
import gc
#import decode
import pytxt2pdf

OLIGO_SIZE = 117
if hasattr(sys, "frozen"):
        PATH = os.path.dirname(sys.executable)
else:
        PATH = os.path.dirname(os.path.abspath(__file__))

#Return the list of ASCII values for given string
def stringToAscii(string):
    string = bytearray(string)
    listx = []
    for i in string:
        listx.append(i)
    return listx


#Given a list of ascii values as input returns the corrosponding string
def asciiToString(listx):
    string = StringIO()
    for i in listx:
        string.write(chr(int(i)))
    return string.getvalue()


#Returns base 3 integer given a number
def decimalToBase3(num):
   if 0 <= num < 3:
       return num
   result = ""
   while num:
       num, digit = divmod(num, 3) 
       result = str(digit) + result
   return int(result)


#Given a decimal number as input this converts it to base4
def decimalToBase4(num):
   if 0 <= num < 4:
       return num
   result = ""
   while num:
       num, digit = divmod(num, 4) 
       result = str(digit) + result
   return int(result)


#Given a base3 number as input this one returns its corrorsponding decimal number
def base3ToDecimal(base3):
    base3 = str(base3)
    decimal = 0
    count = len(base3) - 1
    for i in base3:
        if i != '1' and i != '2' and i != '0':
            #print "Please enter valid base3 number"
            return 0
        decimal = decimal + int(i) * (3 ** count)
        count = count - 1
    return decimal
    

#Given a base4 number as input this one returns its corrorsponding decimal number
def base4ToDecimal(base4):
    base4 = str(base4)
    decimal = 0
    count = len(base4) - 1
    for i in base4:
        if i != '1' and i != '2' and i != '0' and i != '3':
            #print "Please enter valid base4 number"
            return 0
        decimal = decimal + int(i) * (4 ** count)
        count = count - 1
    return decimal


#Given a small number append 0 to its begining to make it of length 20
def decimalOfLength20(num):
    if len(str(num)) <= 20:
        num = str(num)
        while len(num) < 20:
            num = '0' + num
        return num
    else:
        #print "Please enter number of length less than 20!!"
        return num


#Converts ,Huffman dict given ,to Corrosponding String of Base3
def HuffmanToString(listy):
    strx = StringIO()
    for i in xrange(len(listy)):
        strx.write(listy[i])
    return strx.getvalue()


#Converts a base3 String to DNA Base String
def base3ToDNABase(num):
    dnaList = StringIO()
    temp = ''
    if num[0] == '0':
        dnaList.write("C")
        temp = 'C'
    elif num[0] == '1':
        dnaList.write("G")
        temp = 'G'
    elif num[0] == '2':
        dnaList.write("T")
        temp = 'T'
    for i in xrange(1,len(num)):
        if temp == "A":
            if num[i] == '0':
                dnaList.write("C")
                temp = 'C'
            elif num[i] == '1':
                dnaList.write("G")
                temp = 'G'
            elif num[i] == '2':
                dnaList.write("T")
                temp = 'T'
        elif temp == "T":
            if num[i] == '0':
                dnaList.write("A")
                temp = 'A'
            elif num[i] == '1':
                dnaList.write("C")
                temp = 'C'
            elif num[i] == '2':
                dnaList.write("G")
                temp = 'G'
        elif temp == "G":
            if num[i] == '0':
                dnaList.write("T")
                temp = 'T'
            elif num[i] == '1':
                dnaList.write("A")
                temp = 'A'
            elif num[i] == '2':
                dnaList.write("C")
                temp = 'C'
        elif temp == "C":
            if num[i] == '0':
                dnaList.write("G")
                temp = 'G'
            elif num[i] == '1':
                dnaList.write("T")
                temp = 'T'
            elif num[i] == '2':
                dnaList.write("A")
                temp = 'A'
    del num
    #print "DNA conversion puru"
    return dnaList.getvalue()



#Same as above only requires previous Base as char input
def base3ToDNABaseWithChar(num,char):
    dnaList = StringIO()
    if char == "A":
        if num[0] == '0':
            dnaList.write("C")
            char = 'C'
        elif num[0] == '1':
            dnaList.write("G")
            char = 'G'
        elif num[0] == '2':
            dnaList.write("T")
            char = 'T'
    elif char == "T":
        if num[0] == '0':
                dnaList.write("A")
                char = 'A'
        elif num[0] == '1':
                dnaList.write("C")
                char = 'C'
        elif num[0] == '2':
                dnaList.write("G")
                char = 'G'
    elif char == "G":
            if num[0] == '0':
                dnaList.write("T")
                char = 'T'
            elif num[0] == '1':
                dnaList.write("A")
                char = 'A'
            elif num[0] == '2':
                dnaList.write("C")
                char = 'C'
    elif char == "C":
            if num[0] == '0':
                dnaList.write("G")
                char = 'G'
            elif num[0] == '1':
                dnaList.write("T")
                char = 'T'
            elif num[0] == '2':
                dnaList.write("A")
                char = 'A'
    for i in xrange(1,len(num)):
        if char == "A":
            if num[i] == '0':
                dnaList.write("C")
                char = 'C'
            elif num[i] == '1':
                dnaList.write("G")
                char = 'G'
            elif num[i] == '2':
                dnaList.write("T")
                char = 'T'
        elif char == "T":
            if num[i] == '0':
                dnaList.write("A")
                char = 'A'
            elif num[i] == '1':
                dnaList.write("C")
                char = 'C'
            elif num[i] == '2':
                dnaList.write("G")
                char = 'G'
        elif char == "G":
            if num[i] == '0':
                dnaList.write("T")
                char = 'T'
            elif num[i] == '1':
                dnaList.write("A")
                char = 'A'
            elif num[i] == '2':
                dnaList.write("C")
                char = 'C'
        elif char == "C":
            if num[i] == '0':
                dnaList.write("G")
                char = 'G'
            elif num[i] == '1':
                dnaList.write("T")
                char = 'T'
            elif num[i] == '2':
                dnaList.write("A")
                char = 'A'
    return dnaList.getvalue()



#Returns the string of length 100 starting from given index
def stringOfLength100(index,string):
    if (len(string) - index) < 100:
        #print "Enter proper string/index of sufficient length"
        return string
    else:
        string1 = StringIO()
        string1.write(string[index : index + 100])
        return string1.getvalue()


#Divides the string into chunks of size 100
def stringToChunks(string):
    f = []
    if len(string) > 100:
        i = xrange((len(string)/25) - 3)
        for j in i:
            f.append(stringOfLength100(25*j,string))
    else:
        f = [string]
    return f


#Assuming reverse compliment IUPAC version
#A->T
#T->A
#C->G
#G-C
def reverseCompliment(string):
    string1 = StringIO()
    for i in xrange(len(string)):
        if string[i] == 'A':
            string1.write('T')
        elif string[i] == 'T':
            string1.write('A')
        elif string[i] == 'G':
            string1.write('C')
        else:
            string1.write('G')
    return string1.getvalue()


#Returns the new list with appended index info
def appendIndexInfo(listx):
    #print listx
    base3List = genIndexList(len(listx),12)
    for i in xrange(len(base3List)):
        if len(listx[0]) >= 100:
            string = base3ToDNABaseWithChar(base3List[i],listx[i][99])
        elif len(listx[0]) == 25:
            string = base3ToDNABaseWithChar(base3List[i],listx[i][24])
        elif len(listx[0]) == 50:
            string = base3ToDNABaseWithChar(base3List[i],listx[i][49])
        elif len(listx[0]) == 75:
            string = base3ToDNABaseWithChar(base3List[i],listx[i][74])
        listx[i] = listx[i] + string
    #print len(listx[1])
    del base3List
    return listx
    

#Returns the list of indexes
def genIndexList(length, ID):
    indexInfoList = []
    ID = str(ID)
    for i in xrange(length):
        i3 = format(decimalToBase3(i), '012d')
        p = (int(ID[0]) + int(i3[0]) + int(i3[2]) + int(i3[4]) + int(i3[6]) + int(i3[8]) + int(i3[10]))%3
        indexInfoList.append('{}{}{}'.format(ID, i3, p))

    del i3
    del p
    del ID
    return indexInfoList


#IF even chunk no then append A else T and prepend G else C
def appendPrepend(listx):
    for i in xrange(len(listx)):
        if i%2 == 0:
            listx[i] = "A" + listx[i] + "G"
        else:
           listx[i] = "T" + listx[i] + "C"
    #print "append Prepend puru!!"
    return listx

#New version to convert string to chunks where in while converting to chunks parity bits are added
def xstringToChunks(string):
	f = []
	if len(string) > 100:
		for j in xrange((len(string)/25) - 3):
			f.append(genErrorChecksForString(stringOfLength100(25*j,string),j,12))
	else:
		f = [string]
	return f


#Take a dna chunk of lenght 100 as input and gives out corrosponding error conditions appended string
def genErrorChecksForString(string,index,ID):
	ID = str(ID)
	if len(string) != 100:
		#print "Error String length :" , len(string)
		return None
	else:
		if index % 2 != 0:
			string = reverseCompliment(string)
		i3 = format(decimalToBase3(index), '012d')
		p = (int(ID[0]) + int(i3[0]) + int(i3[2]) + int(i3[4]) + int(i3[6]) + int(i3[8]) + int(i3[10]))%3
		string = string + base3ToDNABaseWithChar('{}{}{}'.format(ID, i3, p),string[-1])
		
		if index % 2 != 0:
			string =  "T" + string + "C"
		else:
			string =  "A" + string + "G"
		return string

#####################################################################################################
#Decoding Modules 

#COnvert the chunks to corrosponding DNA String
def dnaChunksToDNAString(listx):
    dnaString = StringIO()
    try:
        for i in xrange(len(listx)):
            dnaString.write(listx[i][1:26])
        dnaString.write(listx[i][26:101])
    except IndexError:
        return -1
    return dnaString.getvalue()


#This method returns base3 String given a DNA Base String as its input
def DNABaseToBase3(num):
    #print num
    base3List = StringIO()
    if num[0] == 'C':
        base3List.write("0")
    elif num[0] == 'G':
        base3List.write("1")
    elif num[0] == 'T':
        base3List.write("2")
    for i in xrange(1,len(num)):
        if num[i-1] == "A":
            if num[i] == 'T':
                base3List.write("2")
            elif num[i] == 'G':
                base3List.write("1")
            elif num[i] == 'C':
                base3List.write("0")
        elif num[i-1] == "C":
            if num[i] == 'A':
                base3List.write("2")
            elif num[i] == 'T':
                base3List.write("1")
            elif num[i] == 'G':
                base3List.write("0")
        elif num[i-1] == "G":
            if num[i] == 'A':
                base3List.write("1")
            elif num[i] == 'T':
                base3List.write("0")
            elif num[i] == 'C':
                base3List.write("2")
        elif num[i-1] == "T":
            if num[i] == 'A':
                base3List.write("0")
            elif num[i] == 'C':
               base3List.write("1")
            elif num[i] == 'G':
                base3List.write("2")
    #print base3List
    return base3List.getvalue()


def DNABaseToBase3WithChar(num,char):
	base3List = StringIO()
	if char == "A":
		if num[0] == 'T':
			base3List.write("2")
		elif num[0] == 'G':
			base3List.write("1")
		elif num[0] == 'C':
			base3List.write("0")
	elif char == "C":
		if num[0] == 'A':
			base3List.write("2")
		elif num[0] == 'T':
			base3List.write("1")
		elif num[0] == 'G':
			base3List.write("0")
	elif char == "G":
		if num[0] == 'A':
			base3List.write("1")
		elif num[0] == 'T':
			base3List.write("0")
		elif num[0] == 'C':
			base3List.write("2")
	elif char == "T":
		if num[0] == 'A':
			base3List.write("0")
		elif num[0] == 'C':
			base3List.write("1")
		elif num[0] == 'G':
			base3List.write("2")
	for i in xrange(1,len(num)):
		if num[i-1] == "A":
			if num[i] == 'T':
				base3List.write("2")
			elif num[i] == 'G':
				base3List.write("1")
			elif num[i] == 'C':
				base3List.write("0")
		elif num[i-1] == "C":
			if num[i] == 'A':
				base3List.write("2")
			elif num[i] == 'T':
				base3List.write("1")
			elif num[i] == 'G':
				base3List.write("0")
		elif num[i-1] == "G":
			if num[i] == 'A':
				base3List.write("1")
			elif num[i] == 'T':
				base3List.write("0")
			elif num[i] == 'C':
				base3List.write("2")
		elif num[i-1] == "T":
			if num[i] == 'A':
				base3List.write("0")
			elif num[i] == 'C':
				base3List.write("1")
			elif num[i] == 'G':
				base3List.write("2")
	return base3List.getvalue()

#This function returns the base 3 Strings S1,S2,S3 from the base 3String S4
def s4ToS1S2S3(base3String):
    s1 = StringIO()
    s3 = ""
    if (len(base3String) % 25) == 0:
        length = len(base3String)
        s3 = base3String[-20:]
        lenS1 = base3ToDecimal(int(s3))
        for i in xrange(lenS1):
            s1.write(base3String[i])
        return s1.getvalue()
    else:
        #print "The length of the base 3 string is not the multiple of 25 please check your string"
        return -1

##############################################################################################################
#These methos include import/export csv modules and some other fucntions which are not yet used in version 1.0
def writeListToCsv(dnaList,path):
    dnaList = unicodedata.normalize('NFKD', dnaList).encode('ascii','ignore')
    lists = dnaList.split(",")
    dnaList = [lists[0][2:119]]
    for i in xrange(1,len(lists)-1):
	dnaList.append(lists[i][2:119])
    dnaList.append(lists[len(lists) - 1][2:119])
    del lists
    c = csv.writer(open(path + "/myList.csv","wb"))
    c.writerow([])
    c.writerow(["",""," © Data Generated using DNA Store"])
    c.writerow([])
    c.writerow(["DNA List:","",dnaList[0]])
    for i in xrange(1,len(dnaList)):
	c.writerow(["","",dnaList[i]])
    print "Exported"

def writeStringToCsv(dnaList,path):
    dnaList = unicodedata.normalize('NFKD', dnaList).encode('ascii','ignore')
    lists = dnaList.split(",")
    dnaList = [lists[0][2:119]]
    for i in xrange(1,len(lists)-1):
	dnaList.append(lists[i][2:119])
    dnaList.append(lists[len(lists) - 1][2:119])
    del lists

    print "Lists made"
    dnaString = dnaChunksToDNAString(dnaList)	
    length = len(dnaList)
    del dnaList
    print "Writer Starting"
    
    c = csv.writer(open(path + "/myString.csv","wb"))
    c.writerow(["© Data Generated using DNA Store","","DNA String"])
    c.writerow([])
    print "Divsion incomplete che ke shu?",len(dnaString)
    seg = 0
    for seg in xrange(0,len(dnaString)/100):
       c.writerow(["","",dnaString[(seg * 100) : (100 * seg) + 100]])
    print "seg",seg
    c.writerow(["","",dnaString[(100 * seg) : ]])
    print "Exported"


def saveInDB(filePath,string,dbPath):
	con = lite.connect(dbPath)
	try:
		print "kya che upar ke"
		cur = con.cursor()
		cur.execute('INSERT INTO DNA VALUES(?,?)',(filePath,string))
		del string,filePath
		con.commit()
	except sqlite3.OperationalError:
		print "nicehe"
		cur = con.cursor()
		cur.execute('DROP TABLE IF EXISTS DNA')
		cur.execute('CREATE TABLE DNA(fileName TEXT NOT NULL,dnaString TEXT NOT NULL)')
		cur.execute('INSERT INTO DNA VALUES(?,?)',(filePath,string))
		con.commit()
	if con:
		con.close()
	return True


def readListFromCsv(filePath,path):
  
	with open(filePath, 'rb') as csvfile:
		spamreader = csv.reader(csvfile)
		dnaList = []
		for row in spamreader:
			dnaList.append(row[2])

	dnaString = dnaChunksToDNAString(dnaList)
	del dnaList
	base3String = DNABaseToBase3(dnaString)
	del  dnaString
	s1 = s4ToS1S2S3(base3String)
	del base3String
	asciiList = HuffmanDictionary.base3ToAscii(s1)
	del s1
	string  = asciiToString(asciiList)

	decodedFile = file(path + "/decode","wb")
	decodedFile.write(string)
	decodedFile.close()
	

def readStringFromCsv(filePath,path):
  
	with open(filePath, 'rb') as csvfile:
		spamreader = csv.reader(csvfile)
		dnaString = StringIO()
		for row in spamreader:
			dnaString.write(row[2])

	print len(dnaString.getvalue())
	base3String = DNABaseToBase3(dnaString.getvalue())
	del  dnaString
	s1 = s4ToS1S2S3(base3String)
	del base3String
	asciiList = HuffmanDictionary.base3ToAscii(s1)
	del s1
	string  = asciiToString(asciiList)

	decodedFile = file(path + "/decode","wb")
	decodedFile.write(string)
	decodedFile.close()
	print "OKAY"

######################################################################################################

def getGCContent(path,costPerBase,naContent):
        import decode
        con = sqlite3.connect(PATH + '/../database/prefs.db')
        with con:
                cur = con.cursor()
                WORKSPACE_PATH = cur.execute('SELECT * FROM prefs WHERE id = 8').fetchone()[1]
                if "linux" in sys.platform:
                        WORKSPACE_PATH = unicodedata.normalize('NFKD', WORKSPACE_PATH).encode('ascii','ignore')
                if not os.path.isdir(WORKSPACE_PATH + '/.temp'):
                        os.mkdir(WORKSPACE_PATH +  '/.temp')
                        
	minMaxGC = decode.degenrateDNAListWithGCCount(path,WORKSPACE_PATH)
	try:
		dnaFile = open(WORKSPACE_PATH + '/.temp/dnaString.txt',"rb")
		fileSize = os.path.getsize(WORKSPACE_PATH + '/.temp/dnaString.txt')
		CHUNK_SIZE = 10000000
		if (fileSize % CHUNK_SIZE) == 0:
			if (fileSize/CHUNK_SIZE) == 0:
				noOfFileChunks = 1
			else:
				noOfFileChunks = (fileSize/CHUNK_SIZE)
		else:
			noOfFileChunks = (fileSize/CHUNK_SIZE) + 1 
		#print "No of Chunks" , noOfFileChunks
		
		dnaLength = 0
		noOfGCPairs = 0
		#print "Chunk No : 1"
		
		if noOfFileChunks > 1:
		  
			tempString = dnaFile.read(CHUNK_SIZE)
			noOfGCPairs += tempString.count('G')
			noOfGCPairs += tempString.count('C')
			del tempString
			
			for chunk_number in range(1,noOfFileChunks - 1):
				#print "Chunk No :",chunk_number + 1
				tempString = dnaFile.read(CHUNK_SIZE)
				noOfGCPairs += tempString.count('C')
				noOfGCPairs += tempString.count('G')
				dnaFile.flush()
				del tempString

			#print "Chunk No:",noOfFileChunks
			tempString = dnaFile.read(fileSize - (noOfFileChunks - 1) * CHUNK_SIZE)
			noOfGCPairs += tempString.count('C')
			noOfGCPairs += tempString.count('G')
			
			del tempString
			#print  "Pairs :" ,noOfGCPairs
		else:
			tempString  = dnaFile.read()
			noOfGCPairs += tempString.count('G')
			noOfGCPairs += tempString.count('C')
			
			del tempString
			#print "Pairs :" ,noOfGCPairs
		dnaFile.close()
		
		noOfGCPairs = noOfGCPairs; minGC = (minMaxGC[0] * 100)/OLIGO_SIZE; maxGC = (minMaxGC[1] * 100)/OLIGO_SIZE
		totalPairs = os.path.getsize(WORKSPACE_PATH + "/.temp/dnaString.txt")
		GCContent = (noOfGCPairs * 100.0)/totalPairs
		totalCost = costPerBase * totalPairs
			
		minMeltingPoint = (81.5 + 16.6 * math.log10(naContent) + 0.41 * (minGC) - 600)/OLIGO_SIZE 
		maxMeltingPoint = (81.5 + 16.6 * math.log10(naContent) + 0.41 * (maxGC) - 600)/OLIGO_SIZE 
			
		if 'darwin' in sys.platform:
			details = "File Selected : " + path + "\n\n#Details for the DNA :\n\n-  GC Content(% in DNA String):\t\t\t" + str(GCContent) + "\n-  Total Cost($ of DNA String):\t\t\t" + str(totalCost) + "\n-  Min Melting Point(deg. C/nucleotide):\t\t" + str(minMeltingPoint) + "\n-  Max Melting Point(deg. C/nucleotide):\t\t" + str(maxMeltingPoint)
		else:
			details = "File Selected : " + path + "\n\n#Details for the DNA :\n\n-  GC Content(% in DNA String):\t\t\t" + str(GCContent) + "\n-  Total Cost($ of DNA String):\t\t\t" + str(totalCost) + "\n-   Min Melting Point(℃/nucleotide):\t\t" + str(minMeltingPoint) + "\n-   Max Melting Point(℃/nucleotide):\t\t" + str(maxMeltingPoint)
	
		detailsFile = file(WORKSPACE_PATH + '/.temp/details.txt',"wb")
		detailsFile.write(details + "\n\n ©2013 Generated using DNA-CLOUD." )
		detailsFile.close()
	except MemoryError:
		return None

def exportToPdf(filePath,savePath):
        import decode
        con = sqlite3.connect(PATH + '/../database/prefs.db')
        with con:
                cur = con.cursor()
                WORKSPACE_PATH = cur.execute('SELECT * FROM prefs WHERE id = 8').fetchone()[1]
                if "linux" in sys.platform:
                        WORKSPACE_PATH = unicodedata.normalize('NFKD', WORKSPACE_PATH).encode('ascii','ignore')
                if not os.path.isdir(WORKSPACE_PATH + '/.temp'):
                        os.mkdir(WORKSPACE_PATH +  '/.temp')
                        
	minMaxGC = decode.degenrateDNAListWithGCCount(filePath,WORKSPACE_PATH)
	try:
		dnaFile = open(WORKSPACE_PATH + '/.temp/dnaString.txt',"rb")
		fileSize = os.path.getsize(WORKSPACE_PATH + '/.temp/dnaString.txt')
		CHUNK_SIZE = 10000000
		if (fileSize % CHUNK_SIZE) == 0:
			if (fileSize/CHUNK_SIZE) == 0:
				noOfFileChunks = 1
			else:
				noOfFileChunks = (fileSize/CHUNK_SIZE)
		else:
			noOfFileChunks = (fileSize/CHUNK_SIZE) + 1 
		#print "No of Chunks" , noOfFileChunks
		
		dnaLength = 0
		noOfGCPairs = 0
		#print "Chunk No : 1"
		
		if noOfFileChunks > 1:
		  
			tempString = dnaFile.read(CHUNK_SIZE)
			noOfGCPairs += tempString.count('G')
			noOfGCPairs += tempString.count('C')
			del tempString
			
			for chunk_number in range(1,noOfFileChunks - 1):
				#print "Chunk No :",chunk_number + 1
				tempString = dnaFile.read(CHUNK_SIZE)
				noOfGCPairs += tempString.count('C')
				noOfGCPairs += tempString.count('G')
				dnaFile.flush()
				del tempString

			#print "Chunk No:",noOfFileChunks
			tempString = dnaFile.read(fileSize - (noOfFileChunks - 1) * CHUNK_SIZE)
			noOfGCPairs += tempString.count('C')
			noOfGCPairs += tempString.count('G')
			dnaFile.flush()
		
			del tempString
			#print  "Pairs :" ,noOfGCPairs
		else:
			tempString  = dnaFile.read(fileSize)
			noOfGCPairs += tempString.count('G')
			noOfGCPairs += tempString.count('C')
			
			del tempString
			#print "Pairs :" ,noOfGCPairs
		dnaFile.close()
	except MemoryError:
		return None
	
	detailsFile = file(WORKSPACE_PATH + '/.temp/details.txt',"wb")
	string = "\n\n#DETAILS :- \n- Number of DNA  Chunks :- \t\t\t" + str(minMaxGC[2]) + "\n- Length of DNA String :- \t\t\t" + str(os.path.getsize(WORKSPACE_PATH + '/.temp/dnaString.txt')) +  "\n- GC Content of DNA String :- \t\t" + str((noOfGCPairs * 100.0)/fileSize) + "\n- Amount of DNA required :-\t\t\t" + str(fileSize/10.0 ** 20) + " gms\n- File Size (Bytes) :- \t\t\t\t" + str(os.path.getsize(filePath)) + "\n\n\n\n#DNA CHUNKS :- \n\nSeq_ID\t\t\t\tSequence\n\n"
	detailsFile.write(string)
	
	fileOpened = open(filePath,"rb")
	fileSize = os.path.getsize(filePath)
	CHUNK_SIZE = 10000000
	if (fileSize % CHUNK_SIZE) == 0:
		if (fileSize/CHUNK_SIZE) == 0:
			noOfFileChunks = 1
		else:
			noOfFileChunks = (fileSize/CHUNK_SIZE)
	else:
		noOfFileChunks = (fileSize/CHUNK_SIZE) + 1 
	#print "Writing to PDF\nNo of Chunks" , noOfFileChunks

	counter = 1
	if noOfFileChunks >  1 :
		#print "Chunk No : 1"
		dnaList = fileOpened.read(CHUNK_SIZE)
		prependString = ""
		j = -1
		while True:
			if dnaList[j] == ',':
				break
			prependString = dnaList[j] + prependString
			j -= 1
		#print j , prependString 
		tempList = (dnaList.split(","))[:-1]
		dnaString = StringIO()
		for i in xrange(len(tempList)):
			#dnaString.write(tempList[i] + " - " + str(counter) + ",\n")
			dnaString.write(str(counter) + " - " + tempList[i] + " ,\n")
			counter += 1
		detailsFile.write(dnaString.getvalue())
		
		del tempList
		del dnaString
		del j
		del dnaList
		#print dnaLength
		for chunk_number in xrange(1,noOfFileChunks-1):
			#print "Chunk No :" , chunk_number + 1
			dnaString = StringIO()
			tempList = prependString
			dnaList = fileOpened.read(CHUNK_SIZE)
			prependString = ""
			j = -1
			while True:
				if dnaList[j] == ',':
					break
				prependString = dnaList[j] + prependString
				j -= 1
			#print j , prependString 
			tempList = ((tempList + dnaList).split(","))[:-1]
			
			for i in xrange(len(tempList)):
				#dnaString.write(tempList[i] + " - " + str(counter) + ",\n")
				dnaString.write(str(counter) + " - " + tempList[i] + " ,\n")
				counter += 1
			detailsFile.write(dnaString.getvalue())

			del dnaString
			del tempList
			del j
			del dnaList
			
		#print "Chunk No :",noOfFileChunks
		dnaString = StringIO()
		tempList = prependString
		dnaList = fileOpened.read()
		j = -1
		prependString = ""
		while True:
			if dnaList[j] == ',':
				break
			prependString = dnaList[j] + prependString
			j -= 1
		#print j , prependString 
		tempList = ((tempList + dnaList).split(","))[:-1]
		
		for i in xrange(len(tempList)):
			#dnaString.write(tempList[i] + " - " + str(counter) + ",\n")
			dnaString.write(str(counter) + " - " + tempList[i] + " ,\n")
			counter += 1 
		detailsFile.write(dnaString.getvalue())
		
		del tempList
		del dnaString
		del j
		del dnaList
	else:
		dnaString = StringIO()
		tempList = (fileOpened.read().split(","))[:-1]
		for i in xrange(len(tempList)):
			#dnaString.write(tempList[i] + " - " + str(counter) + ",\n")
			dnaString.write(str(counter) + " - " + tempList[i] + " ,\n")
			counter += 1 
		detailsFile.write(dnaString.getvalue())
		detailsFile.flush()
		#fileOpened.flush()
		
		del tempList
		del dnaString

	detailsFile.close()
	fileOpened.close()

	txt2pdf = pytxt2pdf.pyText2Pdf(WORKSPACE_PATH + '/.temp/details.txt',savePath + ".pdf")
	txt2pdf.Convert()

def exportToLatex(filePath,savePath):
        import decode
        con = sqlite3.connect(PATH + '/../database/prefs.db')
        with con:
                cur = con.cursor()
                WORKSPACE_PATH = cur.execute('SELECT * FROM prefs WHERE id = 8').fetchone()[1]
                if "linux" in sys.platform:
                        WORKSPACE_PATH = unicodedata.normalize('NFKD', WORKSPACE_PATH).encode('ascii','ignore')
                if not os.path.isdir(WORKSPACE_PATH + '/.temp'):
                        os.mkdir(WORKSPACE_PATH +  '/.temp')
                        
        minMaxGC = decode.degenrateDNAListWithGCCount(filePath,WORKSPACE_PATH)
        try:
		dnaFile = open(WORKSPACE_PATH + '/.temp/dnaString.txt',"rb")
		fileSize = os.path.getsize(WORKSPACE_PATH + '/.temp/dnaString.txt')
		CHUNK_SIZE = 10000000
		if (fileSize % CHUNK_SIZE) == 0:
			if (fileSize/CHUNK_SIZE) == 0:
				noOfFileChunks = 1
			else:
				noOfFileChunks = (fileSize/CHUNK_SIZE)
		else:
			noOfFileChunks = (fileSize/CHUNK_SIZE) + 1 
		#print "No of Chunks" , noOfFileChunks
		
		dnaLength = 0
		noOfGCPairs = 0
		#print "Chunk No : 1"
		
		if noOfFileChunks > 1:
		  
			tempString = dnaFile.read(CHUNK_SIZE)
			noOfGCPairs += tempString.count('G')
			noOfGCPairs += tempString.count('C')
			del tempString
			
			for chunk_number in range(1,noOfFileChunks - 1):
				#print "Chunk No :",chunk_number + 1
				tempString = dnaFile.read(CHUNK_SIZE)
				noOfGCPairs += tempString.count('C')
				noOfGCPairs += tempString.count('G')
				dnaFile.flush()
				del tempString

			#print "Chunk No:",noOfFileChunks
			tempString = dnaFile.read(fileSize - (noOfFileChunks - 1) * CHUNK_SIZE)
			noOfGCPairs += tempString.count('C')
			noOfGCPairs += tempString.count('G')
			#dnaFile.flush()
		
			del tempString
			#print  "Pairs :" ,noOfGCPairs
		else:
			tempString  = dnaFile.read(fileSize)
			noOfGCPairs += tempString.count('G')
			noOfGCPairs += tempString.count('C')
			
			del tempString
			#print "Pairs :" ,noOfGCPairs
		dnaFile.close()
	except MemoryError:
		return None

	detailsFile = file(savePath + '.tex',"wb")
	#print filePath
        #string = "\n\n#DETAILS :- \n- Number of DNA  Chunks :- \t\t\t" + str(minMaxGC[2]) + "\n- Length of DNA String :- \t\t\t" + str(os.path.getsize(PATH + '/../.temp/dnaString.txt')) +  "\n- GC Content of DNA String :- \t\t" + str((noOfGCPairs * 100.0)/fileSize) + "\n- Amount of DNA required :-\t\t\t" + str(fileSize/10.0 ** 20) + " gms\n- File Size (Bytes) :- \t\t\t\t" + str(os.path.getsize(filePath)) + "\n\n\n\n#DNA CHUNKS :- \n\nSeq_ID\t\t\t\tSequence\n\n"
	string = """\documentclass[12pt]{article}
\usepackage{pdflscape}
\usepackage{longtable}
%  ############################# Generated using DNA-Cloud
\\topmargin=-30pt
\\textheight=648pt
\oddsidemargin=0pt
\\textwidth=468pt
%  ##############################  © 2013 - Gupta Lab (www.guptalab.org/dnacloud)
\pagestyle{plain}
\\renewcommand{\\baselinestretch}{1.15}
\\begin{document}
\\begin{landscape}
\\begin{center}
{\\bf DNA Cloud Data Sheet\n\nFile: """ + str(filePath.split('\\')[-1])+ """}
\end{center}
\[
\\begin{array}{|l|c|}
\hline
 \mbox{\\bf DNA Properties} & \mbox{\\bf Value} \\\\\hline\hline
\mbox{Number of DNA  Chunks} & """ + str(minMaxGC[2]) +"""\\\\
\mbox{Length of Each DNA  Chunk} & 117 \\\\ 
\mbox{Length of Entire DNA String} &""" + str(os.path.getsize(WORKSPACE_PATH + '/.temp/dnaString.txt')) +""" \\\\
\mbox{GC Content of DNA String} & """ + str((noOfGCPairs * 100.0)/fileSize) +"""\\\\
\mbox{Amount of DNA required} &"""+ str(fileSize/455.0 * (10 ** 18)) +"""\mbox{gms} \\\\
\mbox{File Size (Bytes)} & """+ str(os.path.getsize(filePath)) +"""\\\\
\hline
\end{array}
\]
\\end{landscape}
{\\tiny
\\begin{landscape}
    \centering
   \\begin{longtable}{|l|l|}
   \\hline \\multicolumn{2}{l}{\\textit{\\bf Continued on next page, generate by DNA-Cloud, http://www.guptalab.org/dnacloud}} \\\\
\\endfoot
\\hline
\\endlastfoot
\\hline
   \mbox{\\bf Seq ID} & \mbox{\\bf DNA Chunk Sequence} \\\\\\hline\\hline \n"""
	detailsFile.write(string)
	
	fileOpened = open(filePath,"rb")
	fileSize = os.path.getsize(filePath)
	CHUNK_SIZE = 10000000
	if (fileSize % CHUNK_SIZE) == 0:
		if (fileSize/CHUNK_SIZE) == 0:
			noOfFileChunks = 1
		else:
			noOfFileChunks = (fileSize/CHUNK_SIZE)
	else:
		noOfFileChunks = (fileSize/CHUNK_SIZE) + 1 
	#print "No of Chunks" , noOfFileChunks

	counter = 1
	if noOfFileChunks >  1 :
		#print "Chunk No : 1"
		dnaList = fileOpened.read(CHUNK_SIZE)
		prependString = ""
		j = -1
		while True:
			if dnaList[j] == ',':
				break
			prependString = dnaList[j] + prependString
			j -= 1
		#print j , prependString 
		tempList = (dnaList.split(","))[:-1]
		dnaString = StringIO()
		for i in xrange(len(tempList)):
			#dnaString.write(tempList[i] + " - " + str(counter) + ",\n")
			#dnaString.write(str(counter) + " - " + tempList[i] + " ,\n")
			dnaString.write(str(counter) + " & " + tempList[i] + " , \\\\ \n")
			counter += 1
		detailsFile.write(dnaString.getvalue())
		
		del tempList
		del dnaString
		del j
		del dnaList
		#print dnaLength
		for chunk_number in xrange(1,noOfFileChunks-1):
			#print "Chunk No :" , chunk_number + 1
			dnaString = StringIO()
			tempList = prependString
			dnaList = fileOpened.read(CHUNK_SIZE)
			prependString = ""
			j = -1
			while True:
				if dnaList[j] == ',':
					break
				prependString = dnaList[j] + prependString
				j -= 1
			#print j , prependString 
			tempList = ((tempList + dnaList).split(","))[:-1]
			
			for i in xrange(len(tempList)):
				#dnaString.write(tempList[i] + " - " + str(counter) + ",\n")
				#dnaString.write(str(counter) + " - " + tempList[i] + " ,\n")
				dnaString.write(str(counter) + " & " + tempList[i] + " , \\\\ \n")
				counter += 1
			detailsFile.write(dnaString.getvalue())

			del dnaString
			del tempList
			del j
			del dnaList
			
		#print "Chunk No :",noOfFileChunks
		dnaString = StringIO()
		tempList = prependString
		dnaList = fileOpened.read()
		j = -1
		prependString = ""
		while True:
			if dnaList[j] == ',':
				break
			prependString = dnaList[j] + prependString
			j -= 1
		#print j , prependString 
		tempList = ((tempList + dnaList).split(","))[:-1]
		
		for i in xrange(len(tempList)):
			#dnaString.write(tempList[i] + " - " + str(counter) + ",\n")
			#dnaString.write(str(counter) + " - " + tempList[i] + " ,\n")
			dnaString.write(str(counter) + " & " + tempList[i] + " , \\\\ \n")
			counter += 1 
		detailsFile.write(dnaString.getvalue())
		
		del tempList
		del dnaString
		del j
		del dnaList
	else:
		dnaString = StringIO()
		tempList = (fileOpened.read().split(","))[:-1]
		for i in xrange(len(tempList)):
			#dnaString.write(tempList[i] + " - " + str(counter) + ",\n")
			#dnaString.write(str(counter) + " - " + tempList[i] + " ,\n")
			dnaString.write(str(counter) + " & " + tempList[i] + " , \\\\ \n")
			counter += 1 
		detailsFile.write(dnaString.getvalue())
		detailsFile.flush()
		#fileOpened.flush()
		
		del tempList
		del dnaString
        detailsFile.write(""" \\hline
    \\end{longtable}
{\\bf Generated by DNA-Cloud, http://www.guptalab.org/dnacloud}
\\end{landscape}
}
\\end{document}""")
	detailsFile.close()
	fileOpened.close()

"""   
#This are the older version of some modules
def genIndexList(length,ID):
    #i3List = []
    print length
    #P = []
    indexInfoList = []
    id = list(str(ID))
    for i in xrange(length):
        i3 = (str(decimalToBase3(i)))
        while len(i3) <= 12:
            i3 = '0' + i3
        i3String = i3
        #for j in i3:
        #    i3String = i3String + str(j)
        p = (int(str(ID)[0]) + int(i3[0]) + int(i3[2]) + int(i3[4]) + int(i3[6]) + int(i3[8]) + int(i3[10]))%3
        #P.append(p)
        #i3List.append(i3String)
        indexInfoList.append(str(ID)+i3String+str(p))
    #print indexInfoList
    print "Index list made"
    return indexInfoList    

#@profile
def divideStringIntoChunks(string):
    length = len(string)
    count = 100
    seg = 0
    listx = []
    while length - count > 100:
        temp = ''
        for i in xrange(100):
            temp = temp + str(string[i + 100 * seg])
        listx.append(temp)
        seg = seg + 1
        count = count + 100
    temp = ''
    for i in xrange(length - count + 1):
        temp = temp + str(string[i + 100 * seg])
    listx.append(temp)
    #print listx
    return listx
"""
