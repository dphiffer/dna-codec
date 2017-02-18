"""
#########################################################################
Author: Shalin Shah
Project: DNA Cloud
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Date: 5 November 2013
Website: www.guptalab.org/dnacloud
This module contains method to encode a given data file into corrosponding dnac file.
#########################################################################
"""

from cStringIO import StringIO
import sqlite3
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
import extraModules

FILE_EXT = '.dnac'
if hasattr(sys, "frozen"):
        PATH = os.path.dirname(sys.executable)
else:
        PATH = os.path.dirname(os.path.abspath(__file__))
#print PATH , "encode"

def encode(readPath,savePath):
        con = sqlite3.connect(PATH + '/../database/prefs.db')
        with con:
                cur = con.cursor()
                WORKSPACE_PATH = cur.execute('SELECT * FROM prefs WHERE id = 8').fetchone()[1]
                #print WORKSPACE_PATH
                if "linux" in sys.platform or 'darwin' in sys.platform:
                        WORKSPACE_PATH = unicodedata.normalize('NFKD', WORKSPACE_PATH).encode('ascii','ignore')
        
                if not os.path.isdir(WORKSPACE_PATH + '/.temp'):
                        os.mkdir(WORKSPACE_PATH +  '/.temp')

	genDNAString(readPath,WORKSPACE_PATH)
	genDNAChunks(readPath,savePath,WORKSPACE_PATH)
	#print "created"
		
def genDNAString(readPath,WORKSPACE_PATH):
         try:                      
		fileOpened = open(readPath,"rb")
		if "win" in sys.platform and not 'darwin' in sys.platform:
			dnaFile = file(WORKSPACE_PATH + '\.temp\dnaString.txt','wb')
		elif "linux" in sys.platform or 'darwin' in sys.platform:
			dnaFile = file(WORKSPACE_PATH + '/.temp/dnaString.txt','wb')
		
		dnaLength = 0
		fileSize = os.path.getsize(readPath)
		fileOpened.seek(0,0)
		CHUNK_SIZE = 10000000
		if (fileSize % CHUNK_SIZE) == 0:
			if (fileSize/CHUNK_SIZE) == 0:
				noOfFileChunks = 1
			else:
				noOfFileChunks = (fileSize/CHUNK_SIZE)
		else:
			noOfFileChunks = (fileSize/CHUNK_SIZE) + 1 
		#print noOfFileChunks
		
		if noOfFileChunks > 1:
                        #print "Chunk No: 1",
                        tempString = StringIO()
			tempString.write(fileOpened.read(CHUNK_SIZE))
			a = extraModules.stringToAscii(tempString.getvalue())
                        huffmanDictionary = HuffmanDictionary.stringToBase3(a)
			S1 = extraModules.HuffmanToString(huffmanDictionary)
			dnaString = extraModules.base3ToDNABase(S1)
			dnaFile.write(dnaString)
			dnaLength = dnaLength + len(S1)
			#fileOpened.flush()
			temp = dnaString[-1]
			
			del tempString
			del S1
			del a
			del huffmanDictionary
			
			for chunk_number in range(1,noOfFileChunks-1):
				#print "Chunk No:",chunk_number + 1
                                tempString = StringIO()
				tempString.write(fileOpened.read(CHUNK_SIZE))
					
				a = extraModules.stringToAscii(tempString.getvalue())
				huffmanDictionary = HuffmanDictionary.stringToBase3(a)
				S1 = extraModules.HuffmanToString(huffmanDictionary)
				dnaString = extraModules.base3ToDNABaseWithChar(S1,temp)
				dnaFile.write(dnaString)
				dnaLength = dnaLength + len(S1)
				dnaFile.flush()
				#fileOpened.flush()
				temp = dnaString[-1]

				del S1
				del huffmanDictionary
				del a
				del tempString
				
			#print "Chunk No:",noOfFileChunks
			
			tempString =StringIO()
			tempString.write(fileOpened.read(CHUNK_SIZE))
			a = extraModules.stringToAscii(tempString.getvalue())
			huffmanDictionary = HuffmanDictionary.stringToBase3(a)
			S1 = extraModules.HuffmanToString(huffmanDictionary)
			dnaString = extraModules.base3ToDNABaseWithChar(S1,temp)
			dnaFile.write(dnaString)
			dnaLength = dnaLength + len(S1)
			dnaFile.flush()
			#fileOpened.flush()
			
			del S1
			del huffmanDictionary
			del a
			del tempString
		else:
			#print "Chunk No: 1",
			tempString = StringIO()
			tempString.write(fileOpened.read())
			a = extraModules.stringToAscii(tempString.getvalue())
			huffmanDictionary = HuffmanDictionary.stringToBase3(a)
			S1 = extraModules.HuffmanToString(huffmanDictionary)
			dnaString = extraModules.base3ToDNABase(S1)
			dnaFile.write(dnaString)
			dnaLength = dnaLength + len(S1)
			#fileOpened.flush()
			
			del tempString
			del S1
			del a
			del huffmanDictionary		
		fileOpened.close()
		gc.collect()
		length = extraModules.decimalToBase3(dnaLength)
		S2 = extraModules.decimalOfLength20(length)
		length = dnaLength + len(S2)
		temp = length
		sx = ""
		while temp % 25 != 0:
			sx = sx + "0"
			temp = temp + 1
		S3 = sx
			
		S4 = S3 + S2
		dnaFile.write(extraModules.base3ToDNABaseWithChar(S4,dnaString[-1]))
		dnaFile.flush()
		dnaFile.close()

		#print "DNA length", dnaLength
		#print "List" , (dnaLength + len(S4))/25 - 3
		#print "List" , os.path.getsize(PATH + '/../.temp/dnaString.txt')/25 - 3
	 except MemoryError:
		return -1

def genDNAChunks(readPath,path,WORKSPACE_PATH):
	try:
		xtemp = readPath.split(".")
		if "win" in sys.platform and not 'darwin' in sys.platform:
			fileOpened = open(WORKSPACE_PATH + '\.temp\dnaString.txt',"rb")
			fileSize = os.path.getsize(WORKSPACE_PATH + '\.temp\dnaString.txt')
		elif "linux" in sys.platform or 'darwin' in sys.platform:
			fileOpened = open(WORKSPACE_PATH + '/.temp/dnaString.txt',"rb")
			fileSize = os.path.getsize(WORKSPACE_PATH + '/.temp/dnaString.txt')
		dnaFile = file(path + "." + xtemp[len(xtemp) - 1] + FILE_EXT,'wb')
		
		dnaListLength = 0
		
		CHUNK_SIZE = 10000000
		if (fileSize % CHUNK_SIZE) == 0:
			if (fileSize/CHUNK_SIZE) == 0:
				noOfFileChunks = 1
			else:
				noOfFileChunks = (fileSize/CHUNK_SIZE)
		else:
			noOfFileChunks = (fileSize/CHUNK_SIZE) + 1 
		#print "No of Chunks :-",noOfFileChunks
		
		if noOfFileChunks > 1:
                        #print "Chunk No: 1"
			tempString = StringIO()
			tempString.write(fileOpened.read(CHUNK_SIZE))
			prependString = ""
			dnaString = tempString.getvalue()
		
			dnaList = extraModules.xstringToChunks(dnaString)
			dnaListLength = dnaListLength + len(dnaList)
			dnaList = str(dnaList)
			dnaFile.write(dnaList[1:-1])
			dnaFile.write(",")
			prependString = dnaString[-75:]
				
			#fileOpened.flush()
			dnaFile.flush()

			#print len(dnaString)/25 - 3 , len(dnaList)
			del tempString
			del dnaString
			del dnaList	
		
			for chunk_number in range(1,noOfFileChunks-1):
				#print "Chunk No:",chunk_number + 1
				tempString = StringIO()
				tempString.write(prependString)
				tempString.write(fileOpened.read(CHUNK_SIZE))
				prependString = ""
			#for i in fileToChunks.file_block(fileOpened, noOfFileChunks, chunk_number):
			#	tempList.write(i)
			#f = extraModules.stringToChunks(tempList.getvalue())
			#fCompliment = extraModules.appendIndexInfo(f)
			#fDoubleCompliment = extraModules.appendPrepend(fCompliment)
				dnaString = tempString.getvalue()
				dnaList = extraModules.xstringToChunks(dnaString)
				dnaListLength = dnaListLength + len(dnaList)
				dnaList = str(dnaList)
				dnaFile.write(dnaList[1:-1])
				dnaFile.write(",")
				prependString = dnaString[-75:]
				
				#fileOpened.flush()
				dnaFile.flush()

				del tempString
				del dnaString
				del dnaList
		
			#print "Chunk No:",noOfFileChunks
			tempString = StringIO()
			tempString.write(prependString)
			tempString.write(fileOpened.read())
			dnaString = tempString.getvalue()
			dnaList = extraModules.xstringToChunks(dnaString)
			dnaListLength = dnaListLength + len(dnaList)
			dnaList = str(dnaList)
			dnaFile.write(dnaList[1:-1])
			dnaFile.write(",")
			
			#fileOpened.flush()
			dnaFile.flush()

			del prependString
			del tempString
			del dnaString
			del dnaList
		else:
			#print "Chunk No: 1"
			tempString = StringIO()
			tempString.write(fileOpened.read())
			prependString = ""
			dnaString = tempString.getvalue()
		
			dnaList = extraModules.xstringToChunks(dnaString)
			dnaListLength = dnaListLength + len(dnaList)
			dnaList = str(dnaList)
			dnaFile.write(dnaList[1:-1])
			dnaFile.write(",")
				
			#fileOpened.flush()
			dnaFile.flush()
				
			del tempString
			del dnaString
			del dnaList	
		#print dnaListLength , "List"
		gc.collect()
		fileOpened.close()  
		dnaFile.close()
		
		return
	except MemoryError:
		return -1
#encode('/Users/administrator/Desktop/Mac Pro.rtf','/Users/administrator/Desktop/abcd')
"""
		#Trivial method to encode where in the entire file is taken as input on a whole if want to try this just copy paste this one in onChoose method of mainFrame.py
		try:
			fileOpened = open(path,"rb")
			self.pnl.txt.WriteText(path)             
			del path

			progressMax = 100
			dialog = wx.ProgressDialog("Note!", "Your file is being converted to DNA String, Please Wait ..", progressMax,style=wx.PD_CAN_ABORT | wx.PD_APP_MODAL)
			keepGoing = True
			count = 0
		
			read = fileOpened.read()
			fileOpened.close()
			print "Read Memory : " , mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]
			a = extraModules.stringToAscii(read)
			self.pnl.txt5.WriteText(str(len(read)))                
			del read
			print "Ascii Memory : " , mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]
		
			self.huffmanDictionary = HuffmanDictionary.stringToBase3(a)
			del a
			print "Huffman Memory : " , mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]
			self.S1 = extraModules.HuffmanToString(self.huffmanDictionary)
			del self.huffmanDictionary
			print "huffman to string Memory : " , mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]
		
			length = extraModules.decimalToBase3(len(self.S1))
			self.S2 = extraModules.decimalOfLength20(length)
		
			length = len(self.S1) + len(self.S2)
			temp = length
			sx = ""
			while temp % 25 != 0:
				sx = sx + "0"
				temp = temp + 1
			self.S3 = sx
				
			self.S4 = self.S1 + self.S3 + self.S2
			self.pnl.txt2.WriteText(str(len(self.S4)))
			del self.S1
			del self.S2
			del self.S3
			print "s1s2s3 memory : " , mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]
			count = count + 25
			keepGoing = dialog.Update(count)
			
			self.dnaString = extraModules.base3ToDNABase(self.S4)
			print "DNA Memory : " ,  mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]
			thread.start_new(self.writeTempString,(self.dnaString,))
			del self.S4
			print len(self.dnaString)

			count = count + 25
			keepGoing = dialog.Update(count)
		
			self.f = extraModules.stringToChunks(self.dnaString)
			count = count + 25
			keepGoing = dialog.Update(count)
			del self.dnaString
			print "Chunks Memory :" ,mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]

			self.fCompliment = extraModules.appendIndexInfo(self.f)
			count = count + 12
			keepGoing = dialog.Update(count)
			del self.f
			print "Index Memory :", mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]

			self.fDoubleCompliment = extraModules.appendPrepend(self.fCompliment)
			count = count + 25
			keepGoing = dialog.Update(count)
			del self.fCompliment
			print "Append Prepend :", mem1 - psutil.virtual_memory()[4]
			mem1 = psutil.virtual_memory()[4]

			noOfChunks = len(self.fDoubleCompliment)
			self.pnl.txt3.WriteText(`noOfChunks`)
			self.pnl.txt4.WriteText(`len(self.fDoubleCompliment[0])`)
			thread.start_new(self.writeTempList,(self.fDoubleCompliment,noOfChunks,))

			count = count + 13
			keepGoing = dialog.Update(count)
  
			dialog.Destroy()
			print "Done!!"
			print time.time() - time1
			print mem1 - psutil.virtual_memory()[4]

		except MemoryError:
			wx.MessageBox('MemoryError Please free up ypur memory or use swap memory or increase RAM', 'Information!',wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP) 
		"""
