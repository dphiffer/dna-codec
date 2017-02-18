"""
Author: Shalin Shah
Project: DNA Cloud
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Date: 5 November 2013
Website: www.guptalab.org/dnacloud
This module contains method to decode the given dnac file.
"""


from cStringIO import StringIO
import sqlite3
import sqlite3 as lite
import unicodedata
import time
import csv
import sys
import HuffmanDictionary
import wx
#import psutil
import thread
import os
import gc
import extraModules

if hasattr(sys, "frozen"):
        PATH = os.path.dirname(sys.executable)
else:
        PATH = os.path.dirname(os.path.abspath(__file__))
#print PATH , "decode"

def decode(readPath,savePath):
        con = sqlite3.connect(PATH + '/../database/prefs.db')
        with con:
                cur = con.cursor()
                WORKSPACE_PATH = cur.execute('SELECT * FROM prefs WHERE id = 8').fetchone()[1]
                if "linux" in sys.platform:
                        WORKSPACE_PATH = unicodedata.normalize('NFKD', WORKSPACE_PATH).encode('ascii','ignore')
                if not os.path.isdir(WORKSPACE_PATH + '/.temp'):
                        os.mkdir(WORKSPACE_PATH +  '/.temp')
                        
	degenrateDNAList(readPath,WORKSPACE_PATH)
	degenrateDNAString(readPath,savePath,WORKSPACE_PATH)
	
def degenrateDNAString(readPath,savePath,WORKSPACE_PATH):
	try:
		xtemp = readPath.split(".")
		if "win" in sys.platform and not 'darwin' in sys.platform:
			dnaFile = open(WORKSPACE_PATH + '\.temp\dnaString.txt',"rb")
			fileSize = os.path.getsize(WORKSPACE_PATH + '\.temp\dnaString.txt')
		elif "linux" in sys.platform or 'darwin' in sys.platform:
			dnaFile = open(WORKSPACE_PATH + '/.temp/dnaString.txt',"rb")
			fileSize = os.path.getsize(WORKSPACE_PATH + '/.temp/dnaString.txt')
		#decodedFile = file(PATH + '\\..\\decodedFiles\\decode','wb')
		if len(xtemp) == 3:
			decodedFile = file(savePath+ "." + xtemp[1],'wb')
		else:
                        decodedFile = file(savePath,'wb')
		
		
		dnaFile.seek(fileSize - 21,0)
		temp = dnaFile.read()
		temp = extraModules.DNABaseToBase3WithChar(temp[1:],temp[0])
		dnaLength = extraModules.base3ToDecimal(temp)
		
		fileSize = dnaLength
		dnaFile.seek(0,0)
		CHUNK_SIZE = 5000000
		if (fileSize % CHUNK_SIZE) == 0:
			if (fileSize/CHUNK_SIZE) == 0:
				noOfFileChunks = 1
			else:
				noOfFileChunks = (fileSize/CHUNK_SIZE)
		else:
			noOfFileChunks = (fileSize/CHUNK_SIZE) + 1 
		#print "No of Chunks" , noOfFileChunks
		
		dnaLength = 0
		#print "Chunk No : 1"
		if noOfFileChunks > 1:
		  
			tempString = StringIO()
			tempString.write(dnaFile.read(CHUNK_SIZE))
			dnaString = tempString.getvalue()
			base3String = extraModules.DNABaseToBase3(dnaString)
			asciiList = HuffmanDictionary.base3ToAscii(base3String)
			j = 0
			prependString = ""
			while asciiList == None:
				j = j-1
				asciiList = HuffmanDictionary.base3ToAscii(base3String[0:j])
				prependString = dnaString[j] + prependString
			string  = extraModules.asciiToString(asciiList)
			decodedFile.write(string)
			temp = dnaString[-1]

			del tempString
			del asciiList
			del string
		
			for chunk_number in range(1,noOfFileChunks - 1):
				#print "Chunk No :",chunk_number + 1
				tempString = StringIO()
				tempString.write(prependString)
				tempString.write(dnaFile.read(CHUNK_SIZE))
				#for i in fileToChunks.file_block(dnaFile, noOfFileChunks, chunk_number):
				#	tempString.write(i)
				#	dnaLength = dnaLength + len(i)
				dnaString = tempString.getvalue()
				base3String = extraModules.DNABaseToBase3WithChar(dnaString,temp)
				asciiList = HuffmanDictionary.base3ToAscii(base3String)
				j = 0
				prependString = ""
				while asciiList == None:
					j = j-1
					asciiList = HuffmanDictionary.base3ToAscii(base3String[0:j])
					prependString = dnaString[j] + prependString
				string  = extraModules.asciiToString(asciiList)
				decodedFile.write(string)
				#dnaFile.flush()
				decodedFile.flush()
				temp = dnaString[j-1]
				
				del string
				del asciiList
				del tempString
				del dnaString
				del base3String
				
			#print "Chunk No:",noOfFileChunks
			tempString = StringIO()
			tempString.write(prependString)
			tempString.write(dnaFile.read(fileSize - (noOfFileChunks - 1) * CHUNK_SIZE))
			
			dnaString = tempString.getvalue()
			base3String = extraModules.DNABaseToBase3WithChar(dnaString,temp)
			asciiList = HuffmanDictionary.base3ToAscii(base3String)
			string  = extraModules.asciiToString(asciiList)
			decodedFile.write(string)
			#dnaFile.flush()
			decodedFile.flush()

			del string
			del asciiList
			del tempString
			del prependString
			del dnaString
		else:
			tempString = StringIO()
			tempString.write(dnaFile.read(fileSize))
			dnaString = tempString.getvalue()
			base3String = extraModules.DNABaseToBase3(dnaString)
			asciiList = HuffmanDictionary.base3ToAscii(base3String)
			string  = extraModules.asciiToString(asciiList)
			decodedFile.write(string)

			del tempString
			del asciiList
			del string
		
		decodedFile.close()
		dnaFile.close()
	except MemoryError:
		return -1

def degenrateDNAList(readPath,WORKSPACE_PATH):
	try:
		fileOpened = open(readPath,"rb")
		#dnaFile = None
		if "win" in sys.platform and not 'darwin' in sys.platform:
			dnaFile = file(WORKSPACE_PATH + "\.temp\dnaString.txt","wb")
		elif "linux" in sys.platform or 'darwin' in sys.platform:
			dnaFile = file(WORKSPACE_PATH + "/.temp/dnaString.txt","wb")

		dnaLength = 0
		#fileSize = os.path.getsize(PATH + "/../.temp/dnaList.txt")
		fileSize = os.path.getsize(readPath)
		CHUNK_SIZE = 10000000
		if (fileSize % CHUNK_SIZE) == 0:
			if (fileSize/CHUNK_SIZE) == 0:
				noOfFileChunks = 1
			else:
				noOfFileChunks = (fileSize/CHUNK_SIZE)
		else:
			noOfFileChunks = (fileSize/CHUNK_SIZE) + 1 
		#print "No of Chunks" , noOfFileChunks
		
		if noOfFileChunks > 1:
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
			tempList = dnaList[:j].split(",")
			dnaString = StringIO()
			for i in xrange(len(tempList)):
                                if tempList[i][0] != " ":
					if tempList[i][1] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][2:27]))
						dnaLength += 25
					else:
						dnaString.write(tempList[i][2:27])
						dnaLength += 25
				else:
					if tempList[i][2] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][3:28]))
						dnaLength += 25
					else:
						dnaString.write(tempList[i][3:28])
						dnaLength += 25
			dnaFile.write(dnaString.getvalue())
			dnaFile.flush()
			#fileOpened.flush()
			
			del tempList
			del dnaString
			del j
			del dnaList
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
				tempList = (tempList + dnaList[:j]).split(",")
				
				for i in xrange(len(tempList)):
					if tempList[i][0] != " ":
						if tempList[i][1] == "T":
							dnaString.write(extraModules.reverseCompliment(tempList[i][2:27]))
							dnaLength += 25
						else:
							dnaString.write(tempList[i][2:27])
							dnaLength += 25
					else:
						if tempList[i][2] == "T":
							dnaString.write(extraModules.reverseCompliment(tempList[i][3:28]))
							dnaLength += 25
						else:
							dnaString.write(tempList[i][3:28])
							dnaLength += 25

				dnaFile.write(dnaString.getvalue())
				dnaFile.flush()
				#fileOpened.flush()
				
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
			tempList = (tempList + dnaList[:j]).split(",")

			for i in xrange(len(tempList)):
				if tempList[i][0] != " ":
					if tempList[i][1] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][2:27]))
						dnaLength += 25
					else:
						dnaString.write(tempList[i][2:27])
						dnaLength += 25
				else:
					if tempList[i][2] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][3:28]))
						dnaLength += 25
					else:
						dnaString.write(tempList[i][3:28])
						dnaLength += 25
			
			if tempList[len(tempList) - 1][0] != " ":
				if tempList[len(tempList) - 1][1] == "T":
					dnaString.write(extraModules.reverseCompliment(tempList[len(tempList) - 1][27:102]))
					dnaLength += 75
				else:
					dnaString.write(tempList[len(tempList) - 1][27:102])
					dnaLength += 75
			else:
				if tempList[len(tempList) - 1][2] == "T":
					dnaString.write(extraModules.reverseCompliment(tempList[len(tempList) - 1][28:103]))
					dnaLength += 75
				else:
					dnaString.write(tempList[len(tempList) - 1][28:103])
					dnaLength += 75
			dnaFile.write(dnaString.getvalue())
			dnaFile.flush()
			#fileOpened.flush()
			
			del tempList
			del dnaString
			del j
			del dnaList
		else:
			dnaList = fileOpened.read()
			prependString = ""
			i = -1
			while True:
				if dnaList[i] == ',':
					break
				prependString = dnaList[i] + prependString
				i -= 1
			#print i , prependString
		  
			tempList = dnaList[:i].split(",")
			dnaString = StringIO()
			#print tempList
			for i in xrange(len(tempList)):
				dnaLength += 25
				if tempList[i][0] != " ":
					if tempList[i][1] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][2:27]))
					else:
						dnaString.write(tempList[i][2:27])
				else:
					if tempList[i][2] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][3:28]))
					else:
						dnaString.write(tempList[i][3:28])
			if tempList[len(tempList) - 1][0] != " ":
				if tempList[len(tempList) - 1][1] == "T":
					dnaString.write(extraModules.reverseCompliment(tempList[len(tempList) - 1][27:102]))
				else:
					dnaString.write(tempList[len(tempList) - 1][27:102])
			else:
				if tempList[len(tempList) - 1][2] == "T":
					dnaString.write(extraModules.reverseCompliment(tempList[len(tempList) - 1][28:103]))
				else:
					dnaString.write(tempList[len(tempList) - 1][28:103])
			dnaLength += 75
			
			dnaFile.write(dnaString.getvalue())
			dnaFile.flush()
			#fileOpened.flush()
			
		fileOpened.close()
		dnaFile.close()
	except MemoryError:
		return -1

def degenrateDNAListWithGCCount(readPath,WORKSPACE_PATH):
	try:
		fileOpened = open(readPath,"rb")
		if "win" in sys.platform and not 'darwin' in sys.platform:
			dnaFile = file(WORKSPACE_PATH + "\.temp\dnaString.txt","wb")
		elif "linux" in sys.platform or 'darwin' in sys.platform:
			dnaFile = file(WORKSPACE_PATH + "/.temp/dnaString.txt","w")
		
		dnaLength = 0
		fileSize = os.path.getsize(readPath)
		CHUNK_SIZE = 10000000
		if (fileSize % CHUNK_SIZE) == 0:
			if (fileSize/CHUNK_SIZE) == 0:
				noOfFileChunks = 1
			else:
				noOfFileChunks = (fileSize/CHUNK_SIZE)
		else:
			noOfFileChunks = (fileSize/CHUNK_SIZE) + 1 
		#print "No of Chunks" , noOfFileChunks
		minGC = 117
		maxGC = 0
		GCCount = 0
		listLength = 0
		
		if noOfFileChunks > 1:
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
			tempList = dnaList[:j].split(",")
			listLength += len(tempList)
			dnaString = StringIO()
			for i in xrange(len(tempList)):
				GCCount = 0
				GCCount += tempList[i].count("G")
				GCCount += tempList[i].count("C")
				if minGC > GCCount:
					minGC = GCCount
				if maxGC < GCCount:
					maxGC = GCCount
				if tempList[i][0] != " ":
					if tempList[i][1] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][2:27]))
						dnaLength += 25
					else:
						dnaString.write(tempList[i][2:27])
						dnaLength += 25
				else:
					if tempList[i][2] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][3:28]))
						dnaLength += 25
					else:
						dnaString.write(tempList[i][3:28])
						dnaLength += 25
			dnaFile.write(dnaString.getvalue())
			dnaFile.flush()
			#fileOpened.flush()
			
			del tempList
			del dnaString
			del j
			del dnaList
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
				tempList = (tempList + dnaList[:j]).split(",")
				listLength += len(tempList)
				for i in xrange(len(tempList)):
					GCCount = 0
					GCCount += tempList[i].count("G")
					GCCount += tempList[i].count("C")
					if minGC > GCCount:
						minGC = GCCount
					if maxGC < GCCount:
						maxGC = GCCount
				
					if tempList[i][0] != " ":
						if tempList[i][1] == "T":
							dnaString.write(extraModules.reverseCompliment(tempList[i][2:27]))
							dnaLength += 25
						else:
							dnaString.write(tempList[i][2:27])
							dnaLength += 25
					else:
						if tempList[i][2] == "T":
							dnaString.write(extraModules.reverseCompliment(tempList[i][3:28]))
							dnaLength += 25
						else:
							dnaString.write(tempList[i][3:28])
							dnaLength += 25

				dnaFile.write(dnaString.getvalue())
				dnaFile.flush()
				#fileOpened.flush()
				
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
			tempList = (tempList + dnaList[:j]).split(",")
                        listLength += len(tempList)
			for i in xrange(len(tempList)):
				GCCount = 0
				GCCount += tempList[i].count("G")
				GCCount += tempList[i].count("C")
				if minGC > GCCount:
					minGC = GCCount
				if maxGC < GCCount:
					maxGC = GCCount
			  
				if tempList[i][0] != " ":
					if tempList[i][1] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][2:27]))
						dnaLength += 25
					else:
						dnaString.write(tempList[i][2:27])
						dnaLength += 25
				else:
					if tempList[i][2] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][3:28]))
						dnaLength += 25
					else:
						dnaString.write(tempList[i][3:28])
						dnaLength += 25
			
			if tempList[len(tempList) - 1][0] != " ":
				if tempList[len(tempList) - 1][1] == "T":
					dnaString.write(extraModules.reverseCompliment(tempList[len(tempList) - 1][27:102]))
					dnaLength += 75
				else:
					dnaString.write(tempList[len(tempList) - 1][27:102])
					dnaLength += 75
			else:
				if tempList[len(tempList) - 1][2] == "T":
					dnaString.write(extraModules.reverseCompliment(tempList[len(tempList) - 1][28:103]))
					dnaLength += 75
				else:
					dnaString.write(tempList[len(tempList) - 1][28:103])
					dnaLength += 75
			dnaFile.write(dnaString.getvalue())
			dnaFile.flush()
			#fileOpened.flush()
			
			del tempList
			del dnaString
			del j
			del dnaList
		else:
			dnaList = fileOpened.read()
			prependString = ""
			i = -1
			while True:
				if dnaList[i] == ',':
					break
				prependString = dnaList[i] + prependString
				i -= 1
			#print i , prependString
		  
			tempList = dnaList[:i].split(",")
			dnaString = StringIO()
			listLength += len(tempList)
			for i in xrange(len(tempList)):
				GCCount = 0
				GCCount += tempList[i].count("G")
				GCCount += tempList[i].count("C")
				if minGC > GCCount:
					minGC = GCCount
				if maxGC < GCCount:
					maxGC = GCCount
					
				dnaLength += 25
				if tempList[i][0] != " ":
					if tempList[i][1] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][2:27]))
					else:
						dnaString.write(tempList[i][2:27])
				else:
					if tempList[i][2] == "T":
						dnaString.write(extraModules.reverseCompliment(tempList[i][3:28]))
					else:
						dnaString.write(tempList[i][3:28])
			
			if tempList[len(tempList) - 1][0] != " ":
				if tempList[len(tempList) - 1][1] == "T":
					dnaString.write(extraModules.reverseCompliment(tempList[len(tempList) - 1][27:102]))
				else:
					dnaString.write(tempList[len(tempList) - 1][27:102])
			else:
				if tempList[len(tempList) - 1][2] == "T":
					dnaString.write(extraModules.reverseCompliment(tempList[len(tempList) - 1][28:103]))
				else:
					dnaString.write(tempList[len(tempList) - 1][28:103])
			dnaLength += 75
			
			dnaFile.write(dnaString.getvalue())
			dnaFile.flush()
			#fileOpened.flush()
			
		fileOpened.close()
		dnaFile.close()
		return (minGC, maxGC, listLength)
	except MemoryError:
		return -1
#decode('/Users/administrator/Desktop/abcd.rtf.dnac','/Users/administrator/Desktop/abcd')
"""
#This is the trivial decode method where in entire dna list containing dna file is take as input on a whole instead of dividing it to chunks
		try:
			
			progressMax = 100
			dialog = wx.ProgressDialog("Note!", "Your file is being prepared from DNA Chunks, Please Wait...", progressMax, style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT)
			keepGoing = True
			count = 0
		
			mem1 = psutil.virtual_memory()[4]
			lists = self.dnaList.split(",")
			self.dnaList = [lists[0][2:119]]
			for i in range(1,len(lists)-1):
				self.dnaList.append(lists[i][2:119])
			self.dnaList.append(lists[len(lists) - 1][2:119])
		#print str(len(self.dnaList)) , type(self.dnaList)
			del lists
			
			self.dnaString = extraModules.dnaChunksToDNAString(self.dnaList)
			del self.dnaList
			print "List to String :", mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]

			count = count + 25
			keepGoing = dialog.Update(count)

			base3String = extraModules.DNABaseToBase3(self.dnaString)
			del self.dnaString
			print "String to base3:", mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]

		
			count = count + 25
			keepGoing = dialog.Update(count)
		
			s1 = extraModules.s4ToS1S2S3(base3String)
			del base3String
			print "Original string s1 Memory :", mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]


			count = count + 25
			keepGoing = dialog.Update(count)
		
			asciiList = HuffmanDictionary.base3ToAscii(s1)
			del s1
			print "Huffman to Ascii Memory:", mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]
		
			string  = extraModules.asciiToString(asciiList)
			count = count + 12
			keepGoing = dialog.Update(count)
			print "Ascii to Bytes String Memory :", mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]
		
			decodedFile = file(PATH + "/../decodedFiles/decode"+self.fileExtension,"wb")
			decodedFile.write(string)
			decodedFile.close()
			print "Write Memory :", mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]

			count = count + 13
			keepGoing = dialog.Update(count)
			dialog.Destroy()
		
			wx.MessageBox('File created in the python folder', 'Note!',wx.OK | wx.ICON_INFORMATION| wx.STAY_ON_TOP)
		except MemoryError:
			wx.MessageBox('MemoryError Please free up ypur memory or use swap memory or increase RAM', 'Note!',wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)
"""
