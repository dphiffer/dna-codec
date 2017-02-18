# -*- coding: cp1252 -*-
"""
#########################################################################
Author: Shalin Shah
Project: DNA Cloud
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Date: 5 November 2013
Website: www.guptalab.org/dnacloud
This module contains code for the main GUI Frame.
#########################################################################
"""

import webbrowser
import os
import wx
import sys
import extraModules
import HuffmanDictionary
import sqlite3 as lite
import sqlite3
import gzip
import unicodedata
import gc
import time
import thread
import threading
import multiprocessing
import panels
from multiprocessing.pool import ThreadPool
import encode
import decode
import pytxt2pdf
from datetime import datetime
#if "win" in sys.platform and 'darwin' not in sys.platform:
#        import win32com.shell.shell as shell
#        ASADMIN = 'asadmin'

############################################
#Preferences database has 6 rows:-
#1->Name
#2->Mobile Number
#3->Mail Id
#4->Opened before or this is the first time
#5->Password enabled/disabled
#6->Password Value if Enabled
#7->Default Workspace Enabled/Disabled
#8->Default Workspace Name/Current workspace used
#9->Number of Workspaces
############################################
if hasattr(sys, "frozen"):
        PATH = os.path.dirname(sys.executable)
else:
        PATH = os.path.dirname(os.path.abspath(__file__))
#print PATH,"main"
############################################
FILE_EXT = '.dnac'
SPLASH_TIMEOUT = 2000
VERSION = "1.0"
NAME = "DNA-CLOUD"
OFFICIAL_WEBSITE = 'http://www.guptalab.org/dnacloud'
PRODUCT_LINK = "http://www.guptalab.org/dnacloud/demo"
FEEDBACK_LINK = "https://docs.google.com/forms/d/1YGu_I9z7Z56oAP1enGByBahqs-ItHbLqnBwCoJouOro/viewform"
STATUS_BAR_MESSAGE = "(C) 2013 Gupta Lab - www.guptalab.org/dnacloud"
ABOUT_COPYRIGHT = '(C) 2013 - All rights Reserved.'
KEY_DEVELOPER = 'Shalin Shah'
ICON_ARTIST = 'Foram Joshi - DNA Cloud Icon Artist'
ICON_IDEA = 'Dixita Limbachiya - DNA Cloud Icon Idea'
FB_LINK = "http://www.facebook.com/dnacloud"
TWITTER_LINK = "http://www.twitter.com/guptalab"
YOUTUBE_LINK = "http://www.youtube.com/channel/UC6JJtSNWpGlA9uIFVxEczag"
QUORA_LINK = "http://www.quora.com/Dna-Cloud"

if "linux" in sys.platform:
  ABOUT_DESCRIPTION = "This software acts as a tool to store any file (inlcuding audio, video or picture) into DNA. Currently the software uses algorithms of Goldman et.al.(Goldman, N.; Bertone, P.; Chen, S.; Dessimoz, C.; Leproust, E. M.; Sipos, B.; Birney, E. (2013). Towards practical, high-capacity, low-maintenance information storage in synthesized DNA. Nature 494 (7435): 77.80). For more information visit us at"

  DETAILED_LICENSE = "(C) 2013 Manish K Gupta,Laboratory of Natural Information Processing\nDA-IICT, Gandhinagar, Gujarat 382007\nhttp://www.guptalab.org/dnacloud\nEmail: dnacloud@guptalab.org\n\nThis software is available as an open source to academic, non-profit institutions etc. under an open source license\nagreement and may be used only in accordance with the terms of the agreement.Any selling or distribution of the\nprogram or it parts,original or modified, is prohibited without a written permission from Manish K Gupta."

elif "win" in sys.platform and not 'darwin' in sys.platform:  
  ABOUT_DESCRIPTION = "This software acts as a tool to store any file (inlcuding audio, video or picture) into DNA. Currently the software uses algorithms of Goldman et.al.\n(Goldman, N.; Bertone, P.; Chen, S.; Dessimoz, C.; Leproust, E. M.; Sipos, B.; Birney, E. (2013). Towards practical, high-capacity, low-\n-maintenance information storage in synthesized DNA. Nature 494 (7435): 77–80). For more information visit us at "
  
  DETAILED_LICENSE = "(C) 2013 Manish K Gupta,Laboratory of Natural Information Processing\nDA-IICT, Gandhinagar, Gujarat 382007\nhttp://www.guptalab.org/dnacloud\nEmail: dnacloud@guptalab.org\n\nThis software is available as an open source to academic, non-profit institutions etc. under an open source license agreement and may be used only in accordance with the terms of the agreement.\n\nAny selling or distribution of the program or its parts,original or modified, is prohibited without a written permission from Manish K Gupta."
elif 'darwin' in sys.platform:
  ABOUT_DESCRIPTION = "This software acts as a tool to store any file (inlcuding audio, video or picture) into DNA. \nCurrently the software uses algorithms of Goldman et.al.(Goldman, N.; Bertone, P.; Chen, S.; \nDessimoz, C.; Leproust, E. M.; Sipos, B.; Birney, E. (2013). Towards practical, high-capacity,\nlow-maintenance information storage in synthesized DNA. Nature 494 (7435): 77.80). \nFor more information visit us at"

  DETAILED_LICENSE = "(C) 2013 Manish K Gupta,Laboratory of Natural Information Processing\nDA-IICT, Gandhinagar, Gujarat 382007\nhttp://www.guptalab.org/dnacloud\nEmail: dnacloud@guptalab.org\n\nThis software is available as an open source to academic, non-profit institutions etc. under an open source license\nagreement and may be used only in accordance with the terms of the agreement.Any selling or distribution of the\nprogram or it parts,original or modified, is prohibited without a written permission from Manish K Gupta."

#############################################

class MyFrame(wx.Frame):
#########################################################################################	       
#This is the constructor of the main frame all the insitialization and GUI definations are in here	       

        def __init__(self,*args,**kargs):
                super(MyFrame,self).__init__(*args,**kargs)
            
                self.pnl = panels.encodePanel(self)
                self.pnl1 = panels.decodePanel(self)
                self.vBox = wx.BoxSizer(wx.VERTICAL)
                self.vBox.Add(self.pnl,1,wx.EXPAND)
                self.vBox.Add(self.pnl1,1,wx.EXPAND)
                self.SetSizer(self.vBox)
                self.pnl.Hide()
                self.pnl1.Hide()
                self.clear()
                self.Layout()
                
                if "linux" in sys.platform or 'darwin' in sys.platform:
		  ico = wx.Icon(PATH + '/../icons/DNAicon.ico', wx.BITMAP_TYPE_ICO)
		  self.SetIcon(ico)
                elif "win" in sys.platform and not 'darwin' in sys.platform:
		  ico = wx.Icon(PATH + '\..\icons\DNAicon.ico', wx.BITMAP_TYPE_ICO)
		  self.SetIcon(ico)
#Create an instance of Menu bar and instances of menues you want in menuBar
                menuBar = wx.MenuBar()
                fileMenu = wx.Menu()
                self.prefMenu = wx.Menu()
                helpMenu = wx.Menu()
                socialMediaMenu = wx.Menu()
                
                #exportMenu = wx.Menu()
                #exportMenu.Append(41,"Export DNA String..")
                #exportMenu.Append(42,"Export DNA Chunks..")
                
                #importMenu = wx.Menu()
                #importMenu.Append(51,"Import DNA String..")
                #importMenu.Append(52,"Import DNA Chunks..")
                
                estimatorMenu = wx.Menu()
                estimatorMenu.Append(61,"Memory Required (Data File)")
                estimatorMenu.Append(62,"Bio-Chemical Properties (DNA File)")
                
#Add items to the menues by using the Append option after creating the item or using the builtin item                
                fileItem1 = wx.MenuItem(fileMenu,1,"File to &DNA (Encoder)")
                #fileItem1.SetBitmap(wx.Bitmap(PATH + '/../icons/encode.png'))
                fileMenu.AppendItem(fileItem1)
                fileItem2 = wx.MenuItem(fileMenu,2,"DNA to &File (Decoder)")
                #fileItem2.SetBitmap(wx.Bitmap(PATH + '/../icons/decode.png'))
                fileMenu.AppendItem(fileItem2)
                subMenu = fileMenu.AppendMenu(wx.ID_ANY,'Storage E&stimator',estimatorMenu)
                #subMenu.SetBitmap(wx.Bitmap(PATH + '/../icons/estimator.png'))
                fileMenu.AppendSeparator()
                fileItem7 = wx.MenuItem(fileMenu,7,"Export Generated &Barcode")
                #fileItem7.SetBitmap(wx.Bitmap(PATH + '/../icons/barcodeMenu.png'))
                fileMenu.AppendItem(fileItem7)     
                fileItem4 = wx.MenuItem(fileMenu,4,"Export DNA Synthesizer File")
                #fileItem4.SetBitmap(wx.Bitmap(PATH + '/../icons/exportDNA.png'))
                fileMenu.AppendItem(fileItem4)
                fileItem5 = wx.MenuItem(fileMenu,5,"Import DNA Sequencer File")
                #fileItem5.SetBitmap(wx.Bitmap(PATH + '/../icons/importDNA.png'))
                fileMenu.AppendItem(fileItem5)
                fileItem8 = wx.MenuItem(fileMenu,8,"Export Details to PDF")
                #fileItem8.SetBitmap(wx.Bitmap(PATH + '/../icons/pdf.jpg'))
                fileMenu.AppendItem(fileItem8)
                fileItem9 = wx.MenuItem(fileMenu,9,"Export Latex File")
                #fileItem9.SetBitmap(wx.Bitmap(PATH + '/../icons/tex.png'))
                fileMenu.AppendItem(fileItem9)
                #fileMenu.AppendMenu(wx.ID_ANY,'E&xport to CSV',exportMenu)
                #fileMenu.AppendMenu(wx.ID_ANY,'&Import from CSV',importMenu)
                fileItem6 = wx.MenuItem(fileMenu,6,"&Clear Temporary Files")

                #fileItem6.SetBitmap(wx.Bitmap(PATH + '/../icons/clearFiles.png'))
                fileMenu.AppendItem(fileItem6)
                fileMenu.AppendSeparator()
                fileItem3 = wx.MenuItem(fileMenu,3,"&Exit")
                #fileItem3.SetBitmap(wx.Bitmap(PATH + '/../icons/quit.png'))
                fileMenu.AppendItem(fileItem3)     
                
                self.prefItem1 = wx.MenuItem(self.prefMenu,11,"Password Protection",kind= wx.ITEM_CHECK);    #Item check makes this pref checkable
                self.prefMenu.AppendItem(self.prefItem1);         
                prefItem3 = wx.MenuItem(self.prefMenu,13,"Change Password");

                #prefItem3.SetBitmap(wx.Bitmap(PATH + '/../icons/changePassword.png'))
                self.prefMenu.AppendItem(prefItem3);
                self.prefMenu.AppendSeparator()
                prefItem2 = wx.MenuItem(self.prefMenu,12,"User Details")
                #prefItem2.SetBitmap(wx.Bitmap(PATH + '/../icons/userDetails.gif'))
                self.prefMenu.AppendItem(prefItem2)
                prefItem4 = wx.MenuItem(self.prefMenu,14,"Switch Workspace")
                #prefItem4.SetBitmap(wx.Bitmap(PATH + '/../icons/switch.png'))
                self.prefMenu.AppendItem(prefItem4)

                helpItem2 = wx.MenuItem(helpMenu,22,"User Manual")
                #helpItem2.SetBitmap(wx.Bitmap(PATH + '/../icons/manual.jpg'))
                helpMenu.AppendItem(helpItem2)
                helpItem5 = wx.MenuItem(helpMenu,25,"Product Demo")
                #helpItem5.SetBitmap(wx.Bitmap(PATH + '/../icons/demoVideo.png'))
                helpMenu.AppendItem(helpItem5)
                helpItem3 = wx.MenuItem(helpMenu,23,"Product Feedback")
                #helpItem3.SetBitmap(wx.Bitmap(PATH + '/../icons/feedback.png'))
                helpMenu.AppendItem(helpItem3)
                helpItem4 = wx.MenuItem(helpMenu,24,"Credits")
                #helpItem4.SetBitmap(wx.Bitmap(PATH + '/../icons/credits.png'))
                helpMenu.AppendItem(helpItem4)
                helpMenu.AppendSeparator()
                helpItem1 = wx.MenuItem(helpMenu,21,"About Us")
                #helpItem1.SetBitmap(wx.Bitmap(PATH + '/../icons/aboutUs.png'))
                helpMenu.AppendItem(helpItem1)

                socialMediaItem1 = wx.MenuItem(socialMediaMenu,41,"Facebook")
                #socialMediaItem1.SetBitmap(wx.Bitmap(PATH + '/../icons/facebook.bmp'))
                socialMediaItem2 = wx.MenuItem(socialMediaMenu,42,"Twitter")
                #socialMediaItem2.SetBitmap(wx.Bitmap(PATH + '/../icons/twitter.bmp'))
                socialMediaItem3 = wx.MenuItem(socialMediaMenu,43,"Quora")
                #socialMediaItem3.SetBitmap(wx.Bitmap(PATH + '/../icons/quora.bmp'))
		socialMediaItem4 = wx.MenuItem(socialMediaMenu,44,"Youtube Channel")
                socialMediaMenu.AppendItem(socialMediaItem1)
                socialMediaMenu.AppendItem(socialMediaItem2)
                socialMediaMenu.AppendItem(socialMediaItem3)
		socialMediaMenu.AppendItem(socialMediaItem4)
                                                
                menuBar.Append(fileMenu,'&File')
                menuBar.Append(self.prefMenu,'&Preferences')
                menuBar.Append(helpMenu,"&Help")
                menuBar.Append(socialMediaMenu,"F&ollow Us")
                self.SetMenuBar(menuBar)
                
#Create a status Bar which can be used to indicate the progress
                statusBar = self.CreateStatusBar();
                statusBar.SetStatusText(STATUS_BAR_MESSAGE);

#Register methods when menu items are clicked ie bind the method with a menuItem
                self.Bind(wx.EVT_MENU,self.OnQuit,id = 3)
                self.Bind(wx.EVT_MENU,self.exportBarcode,id = 7)
                self.Bind(wx.EVT_MENU,self.newMenuItemEncode,id = 1);
                self.Bind(wx.EVT_CLOSE,self.OnQuit)
                self.Bind(wx.EVT_MENU,self.newMenuItemDecode,id = 2);
                self.Bind(wx.EVT_MENU,self.aboutUs,id = 21)
                self.Bind(wx.EVT_MENU,self.userManuel,id = 22)
                self.Bind(wx.EVT_MENU,self.exportList,id = 4)
                self.Bind(wx.EVT_MENU,self.importList,id = 5)
                self.Bind(wx.EVT_MENU,self.onClear,id = 6)
                self.Bind(wx.EVT_MENU,self.settings,id = 12)
                self.Bind(wx.EVT_MENU,self.credits,id = 24)                
                self.Bind(wx.EVT_MENU,self.enablePassword,id = 11)                
                self.Bind(wx.EVT_MENU,self.changePassword,id = 13)
                #self.Bind(wx.EVT_MENU,self.exportString,id = 41)
                #self.Bind(wx.EVT_MENU,self.exportList,id = 42)
                #self.Bind(wx.EVT_MENU,self.importString,id = 51)
                #self.Bind(wx.EVT_MENU,self.importList,id = 52)
                self.Bind(wx.EVT_MENU,self.productFeedback,id = 23)
                self.Bind(wx.EVT_MENU,self.memEstimator,id = 61)
                self.Bind(wx.EVT_MENU,self.estimator,id = 62)
                self.Bind(wx.EVT_MENU,self.productDemo,id = 25)
                self.Bind(wx.EVT_MENU,self.exportPdf,id = 8)
                self.Bind(wx.EVT_MENU,self.exportLatex,id = 9)
                self.Bind(wx.EVT_MENU,self.followFB,id = 41)
                self.Bind(wx.EVT_MENU,self.followTwitter,id = 42)
                self.Bind(wx.EVT_MENU,self.followQuora,id = 43)
                self.Bind(wx.EVT_MENU,self.followYoutube,id = 44)
                self.Bind(wx.EVT_MENU,self.switchWork,id = 14)
                
                super(MyFrame,self).SetSize((1000,1000))
                super(MyFrame,self).SetTitle(NAME)
                super(MyFrame,self).Show()
                p = wx.Point(200,200)
                super(MyFrame,self).Move(p)

                self.prefs = False
		if "win" in sys.platform and not 'darwin'in sys.platform:
			con = sqlite3.connect(PATH + '\..\database\prefs.db')
			#print "windows"
		elif "linux" in sys.platform or 'darwin' in sys.platform:
			con = sqlite3.connect(PATH + '/../database/prefs.db')
			#print "unix"
		try:
			cur = con.cursor()
			string = (cur.execute('SELECT * FROM prefs WHERE id = 4').fetchone())[1]
			self.hasDefaultWorkspace = (cur.execute('SELECT * FROM prefs WHERE id = 7').fetchone())[1]
			if "linux" in sys.platform:
				string = unicodedata.normalize('NFKD', string).encode('ascii','ignore')
				self.hasDefaultWorkspace = unicodedata.normalize('NFKD', self.hasDefaultWorkspace).encode('ascii','ignore')

			if string == "false":
				self.prefs = True
			
			string = (cur.execute('SELECT * FROM prefs WHERE id = 5').fetchone())[1]
			if string == 'true':
				password = (cur.execute('SELECT * FROM prefs WHERE id = 6').fetchone())[1]
				if "linux" in sys.platform:
					password = unicodedata.normalize('NFKD', password).encode('ascii','ignore')
				result = wx.PasswordEntryDialog(None,'Please Enter Your Password','Password','',wx.OK | wx.CANCEL)
				passwordMatch = False
				while passwordMatch != True:
					match = result.ShowModal()
					if match == wx.ID_OK:
						if password == result.GetValue():
							passwordMatch = True
						else:
							wx.MessageDialog(self,'Your Password is Incorrect please Enter Again', 'Information!',wx.OK |wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
					else:
						result.Destroy()
						sys.exit()
			#self.qrText = ""
			#for i in cur.execute('SELECT * FROM prefs where id < 4'):
			#	if "win" in sys.platform:
			#		self.qrText = self.qrText + i[1] + "\n"
			#	if "linux" in sys.platform:
			#		self.qrText = self.qrText + unicodedata.normalize('NFKD', i[1]).encode('ascii','ignore') + "\n"
			self.isPasswordProtected = cur.execute('SELECT * FROM prefs where id = 5').fetchone()[1]
			if "linux" in sys.platform:
				self.isPasswordProtected = unicodedata.normalize('NFKD', cur.execute('SELECT * FROM prefs where id = 5').fetchone()[1]).encode('ascii','ignore')
			#for i in cur.execute('SELECT * FROM prefs'):
			#	print i
			con.close() 
                except sqlite3.OperationalError:
                        #print "New prefs DB"
			cur.execute('DROP TABLE IF EXISTS prefs')
			cur.execute('CREATE TABLE prefs(id INT,details TEXT)') 
			cur.execute('INSERT INTO prefs VALUES(1,"Your full Name")')
			cur.execute('INSERT INTO prefs VALUES(2,"Cell Phone No")')
			cur.execute('INSERT INTO prefs VALUES(3,"Your mail Id")')
			cur.execute('INSERT INTO prefs VALUES(4,"false")')
			cur.execute('INSERT INTO prefs VALUES(5,"false")')
			cur.execute('INSERT INTO prefs VALUES(6,"password")')
			cur.execute('INSERT INTO prefs VALUES(7,"False")')
			cur.execute('INSERT INTO prefs VALUES(8,"None")')
			cur.execute('INSERT INTO prefs VALUES(9,"0")')
			con.commit()
			self.prefs = True
			#self.qrText = ""
			#for i in cur.execute('SELECT * FROM prefs where id < 4'):
			#	if "win" in sys.platform:
			#		self.qrText = self.qrText + i[1] + "\n"
			#	if "linux" in sys.platform:
			#		self.qrText = self.qrText + unicodedata.normalize('NFKD', i[1]).encode('ascii','ignore') + "\n"
			self.isPasswordProtected = cur.execute('SELECT * FROM prefs where id = 5').fetchone()[1]
			if "linux" in sys.platform:
				self.isPasswordProtected = unicodedata.normalize('NFKD', cur.execute('SELECT * FROM prefs where id = 5').fetchone()[1]).encode('ascii','ignore')
			con.close()
                	self.hasDefaultWorkspace = "False"
		
#First of all asked whether to encode or deocode so display a dialog to ask him what he wants to do
		#self.ask =  panels.chooseDialog(None,101,"Welcome to DNA-CLOUD!")
		#self.ask.encodeBut.Bind(wx.EVT_BUTTON,self.encode)
		#self.ask.decodeBut.Bind(wx.EVT_BUTTON,self.decode)
		#self.ask.ShowModal()

		if self.hasDefaultWorkspace == "False":
			panels.workspaceLauncher(None,101,"Workspace Launcher!").ShowModal()
                if self.prefs:
                        panels.Preferences(None,0,"Your Details").ShowModal()
		
		if self.isPasswordProtected == 'true':
			self.prefMenu.Check(self.prefItem1.GetId(), True)
		else:
			self.prefMenu.Check(self.prefItem1.GetId(), False)
                 
		#self.onUseQrcode(self.qrText) 

##################################################################
#The password modules

	def changePassword(self,e):
		if "win" in sys.platform and not 'darwin' in sys.platform:
			con = sqlite3.connect(PATH + '\..\database\prefs.db')
		elif "linux" in sys.platform or 'darwin' in sys.platform:
			con = sqlite3.connect(PATH + '/../database/prefs.db')
		with con:
			cur = con.cursor()
			password = panels.setPasswordDialog(None,101,"Password").ShowModal()
			if "win" in sys.platform:
				isEnabled = cur.execute('SELECT * FROM prefs where id = 5').fetchone()[1]
			elif "linux" in sys.platform:
				isEnabled = unicodedata.normalize('NFKD', cur.execute('SELECT * FROM prefs where id = 5').fetchone()[1]).encode('ascii','ignore')
			if isEnabled == 'true':
				self.prefMenu.Check(self.prefItem1.GetId(), True)
			elif isEnabled == 'false':
				self.prefMenu.Check(self.prefItem1.GetId(), False)
			
	def enablePassword(self,e):
		if "win" in sys.platform and not 'darwin' in sys.platform:
			con = sqlite3.connect(PATH + '\..\database\prefs.db')
		elif "linux" in sys.platform or 'darwin' in sys.platform:
			con = sqlite3.connect(PATH + '/../database/prefs.db')
		with con:
			cur = con.cursor()
			if self.prefItem1.IsChecked():
				password = panels.setPasswordDialog(None,101,"Password").ShowModal()
			else:
				cur.execute('UPDATE prefs SET details = ? WHERE id = ?',("false",5))
		#con = sqlite3.connect("/home/../database/prefs.db")
			if "win" in sys.platform:
				isEnabled = cur.execute('SELECT * FROM prefs where id = 5').fetchone()[1]
			elif "linux" in sys.platform:
				isEnabled = unicodedata.normalize('NFKD', cur.execute('SELECT * FROM prefs where id = 5').fetchone()[1]).encode('ascii','ignore')
			if isEnabled == 'true':
				self.prefMenu.Check(self.prefItem1.GetId(), True)
			elif isEnabled == 'false':
				self.prefMenu.Check(self.prefItem1.GetId(), False)
 
####################################################################
#Main Encode Function is this 

#This method is basically called whenever you want to encode some file for now let the file be text file
        def encode(self,e):
                self.pnl1.Hide()
                self.pnl.Show()
                self.clear()
                self.Layout()
                self.bindEncodeItems()
                self.ask.Destroy()

           
#When the choose file button is clicked then we come here
	def onChoose(self,e):
                fileSelector = wx.FileDialog(self, message="Choose a file",defaultFile="",style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR )
		if fileSelector.ShowModal() == wx.ID_OK:
			paths = fileSelector.GetPaths()
			#print paths
			self.path = unicodedata.normalize('NFKD', paths[0]).encode('ascii','ignore')                
                else:
                        self.path = None
		fileSelector.Destroy()
		del fileSelector

		#print self.pnl.IsShown(), self.pnl1.IsShown(), type(self.path)
                
		if self.pnl.IsShown() and isinstance(self.path, str):
                        #print "Encode"
			self.pnl.txt.WriteText(self.path)
			self.pnl.txt5.WriteText(str(os.path.getsize(self.path)))
			self.pnl.txt4.WriteText("117")
			self.pnl.txt2.WriteText(str(int(5.5 * os.path.getsize(self.path))))
			self.pnl.txt3.WriteText(str(int(5.5 * os.path.getsize(self.path))/25 - 3))
		elif self.pnl1.IsShown() and isinstance(self.path, str):
                        #print "Decode"
			self.clear()
			self.pnl1.txt.WriteText(self.path)
			self.pnl1.txt2.WriteText(str(int((os.path.getsize(self.path)/117 + 3)*25)))
			self.pnl1.txt3.WriteText(str(int(os.path.getsize(self.path)/117)))

		return

############################################################################
#This are the save cancel button modules

	def save(self,e):

                con = sqlite3.connect(PATH + '/../database/prefs.db')
		try:
			cur = con.cursor()
                        string = (cur.execute('SELECT * FROM prefs where id = 8').fetchone())[1]
                        if "linux" in sys.platform:
                                string = unicodedata.normalize('NFKD', string).encode('ascii','ignore')
                except:
                        string = 'None'
                        
		if not self.pnl.txt.IsEmpty() and string == "None":

			locationSelector = wx.FileDialog(self,"Please select location to save your encoded file",style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
			if locationSelector.ShowModal() == wx.ID_OK:
				paths = locationSelector.GetPath()
				if "win" in sys.platform:
					self.savePath = paths
				elif "linux" in sys.platform:
					self.savePath = unicodedata.normalize('NFKD', paths).encode('ascii','ignore')
				terminated = False
			else:
				terminated = True
			locationSelector.Destroy()
			del locationSelector

                        if 'darwin' in sys.platform:
                                p = threading.Thread(name = "encode", target = encode.encode, args = (self.path,self.savePath,))
                        else:
        			p = multiprocessing.Process(target = encode.encode , args = (self.path,self.savePath,) , name = "Encode Process")
			if not terminated:
				p.start()
				temp = wx.ProgressDialog('Please wait...', 'Encoding the File....This may take several minutes....\n\t....so sit back and relax....',parent = self,style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
				temp.SetSize((450,180))
				if 'darwin' in sys.platform:
                                        while p.isAlive():
                                		time.sleep(0.1)
                                		if not temp.UpdatePulse("Encoding the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
                                			#p.terminate()
                                                        #terminated = True
                                                        wx.MessageDialog(self,'Cannot be stopped.Sorry', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
                                			#break
                                	temp.Destroy()
                                        if not p.isAlive():
                                        	p.join()
                                else:        
        				while len(multiprocessing.active_children()) != 0:
                                                time.sleep(0.1)
        					if not temp.UpdatePulse("Encoding the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
        						p.terminate()
        						terminated = True
        						self.clear()
        						break
               				temp.Destroy()
        				p.join()
        				p.terminate()
			
			if not terminated:
				wx.MessageDialog(self,'File has been created', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
				
		elif not self.pnl.txt.IsEmpty() and string != "None":
			xtime = datetime.now().timetuple()
			self.savePath = string + "/dCloud_encodedFile_" + `xtime[2]` + "_" + `xtime[1]` + "_" + `xtime[0]`

                        if 'darwin' in sys.platform:
                                p = threading.Thread(name = "encode", target = encode.encode, args = (self.path,self.savePath,))
                        else:
        			p = multiprocessing.Process(target = encode.encode , args = (self.path,self.savePath,) , name = "Encode Process")
                        terminated = False
			if not terminated:
				p.start()
				temp = wx.ProgressDialog('Please wait...', 'Encoding the File....This may take several minutes....\n\t....so sit back and relax....',parent = self,style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
				temp.SetSize((450,180))
				if 'darwin' in sys.platform:
                                        while p.isAlive():
                                		time.sleep(0.1)
                                		if not temp.UpdatePulse("Encoding the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
                                			#p.terminate()
                                                        #terminated = True
                                                        wx.MessageDialog(self,'Cannot be stopped.Sorry', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
                                			#break
                                	temp.Destroy()
                                        if not p.isAlive():
                                        	p.join()
                                else:        
        				while len(multiprocessing.active_children()) != 0:
                                                time.sleep(0.1)
        					if not temp.UpdatePulse("Encoding the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
        						p.terminate()
        						terminated = True
        						self.clear()
        						break
               				temp.Destroy()
        				p.join()
        				p.terminate()
			
			if not terminated:
				wx.MessageDialog(self,'File has been created', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
				


			"""
			p = multiprocessing.Process(target = encode.encode , args = (self.path,self.savePath,) , name = "Encode Process")
			terminated = False
			if not terminated:
				p.start()
				temp = wx.ProgressDialog('Please wait...', 'Encoding the File....This may take several minutes....\n\t....so sit back and relax....',parent = self,style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
				temp.SetSize((450,180))
				while len(multiprocessing.active_children()) != 0:
					time.sleep(0.1)
					if not temp.UpdatePulse("Encoding the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
						p.terminate()
						terminated = True
						self.clear()
						break
				temp.Destroy()
				p.join()
				p.terminate()
			
			if not terminated:
				wx.MessageDialog(self,'File has been created', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
			"""
		else:
			wx.MessageDialog(self,'Please Select a file from you file system before Converting', 'Note!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
                              
        def discard(self,e):
                if not self.pnl.txt.IsEmpty():
                        self.clear()
                else:
                        wx.MessageDialog(self,'Please Select a file from you file system before Reseting', 'Note!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()

        def clear(self):
                if self.pnl.IsShown():
                        self.pnl.txt.Clear()
                        self.pnl.txt2.Clear()
                        self.pnl.txt3.Clear()
                        self.pnl.txt4.Clear()
                        self.pnl.txt5.Clear()
                elif self.pnl1.IsShown():
                        self.pnl1.txt.Clear()
                        self.pnl1.txt2.Clear()
                        self.pnl1.txt3.Clear()
                        #self.pnl1.txt4.Clear()
                        #self.pnl1.txt5.Clear()
        
##################################################################
#This is the main decoding part

	def decode(self,e):
		self.pnl.Hide()
		self.pnl1.Show()
		self.bindDecodeItems()
		self.clear()
		self.Layout()
		self.ask.Destroy()
		
        def decodeBut1(self,e):
		try:
			progressMax = 100
			dialog = wx.ProgressDialog("Note!", "Your file is being prepared from DNA Chunks, Please Wait...", progressMax,parent = self, style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
			keepGoing = True
			count = 0

			if not self.pnl1.txt21.IsEmpty():
                                base3String = extraModules.DNABaseToBase3(self.pnl1.txt21.GetString(0,self.pnl1.txt21.GetLastPosition()))
                                count = count + 12
                                keepGoing = dialog.Update(count)
                        else:
                                dialog.Destroy()
				wx.MessageDialog(self,'Error Please write a dna string', 'Note!',wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP).ShowModal()
				return 

			s1 = extraModules.s4ToS1S2S3(base3String)
			count = count + 25
			keepGoing = dialog.Update(count)
			if s1 == -1:
				dialog.Destroy()
				wx.MessageDialog(self,'Error imporper string', 'Note!',wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP).ShowModal()
				return 
			
			asciiList = HuffmanDictionary.base3ToAscii(s1)
			count = count + 13
			keepGoing = dialog.Update(count)
			if asciiList == None:
				dialog.Destroy()
				wx.MessageDialog(self,'Error imporper string', 'Note!',wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP).ShowModal()
				return 
			
			string  = extraModules.asciiToString(asciiList)
			count = count + 25
			keepGoing = dialog.Update(count)
			
			if "win" in sys.platform and not 'darwin' in sys.platform:
				decodedFile = file(PATH + "\..\decodedFiles\decode","wb")
			elif "linux" in sys.platform or 'darwin' in sys.platform:
				decodedFile = file(PATH + "/../decodedFiles/decode","wb")
			decodedFile.write(string)
			decodedFile.close()
			count = count + 25
			keepGoing = dialog.Update(count)
			
			dialog.Destroy()
			wx.MessageDialog(self,'File created in the decoded Files folder', 'Note!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
		except MemoryError:
			wx.MessageDialog(self,'MemoryError Please free up ypur memory or use swap memory or increase RAM', 'Note!',wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP).ShowModal()


#This method is called whenever we have a DNA String to be decoded 
	def decodeBut2(self,e):
                con = sqlite3.connect(PATH + '/../database/prefs.db')
		try:
			cur = con.cursor()
                        string = (cur.execute('SELECT * FROM prefs where id = 8').fetchone())[1]
                        if "linux" in sys.platform:
                                string = unicodedata.normalize('NFKD', string).encode('ascii','ignore')
                except:
                        string = 'None'

        
		if (not self.pnl1.txt.IsEmpty()) and (FILE_EXT in self.pnl1.txt.GetString(0,self.pnl1.txt.GetLastPosition())) and string == 'None':

			locationSelector = wx.FileDialog(self,"Please select location to save your decoded file",style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
			if locationSelector.ShowModal() == wx.ID_OK:
				paths = locationSelector.GetPath()
				if "win" in sys.platform:
					self.savePath = paths
				elif "linux" in sys.platform:
					self.savePath = unicodedata.normalize('NFKD', paths).encode('ascii','ignore')
				terminated = False
			else:
				terminated = True
			locationSelector.Destroy()
			del locationSelector

			if 'darwin' in sys.platform:
                                p = threading.Thread(name = "Decode", target = decode.decode, args = (self.path,self.savePath,))
                        else:
        			p = multiprocessing.Process(target = decode.decode , args = (self.path,self.savePath,) , name = "Decode Process")
        			
			if not terminated:
				p.start()
                                temp = wx.ProgressDialog('Please wait...', 'Decoding the File....This may take several minutes....\n\t....so sit back and relax....',parent = self,style = wx.PD_APP_MODAL |  wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
				temp.SetSize((450,180))
				if 'darwin' in sys.platform:
                                        while p.isAlive():
                                		time.sleep(0.1)
                                		if not temp.UpdatePulse("Decoding the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
                                			#p.terminate()
                                                        #terminated = True
                                                        wx.MessageDialog(self,'Cannot be stopped.Sorry', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
                                			#break
                                	temp.Destroy()
                                        if not p.isAlive():
                                        	p.join()
                                else:        
        				while len(multiprocessing.active_children()) != 0:
                                                time.sleep(0.1)
        					if not temp.UpdatePulse("Decoding the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
        						p.terminate()
        						terminated = True
        						self.clear()
        						break
               				temp.Destroy()
        				p.join()
        				p.terminate()
			
			if not terminated:
				wx.MessageDialog(self,'File has been created', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
				
                        """
			if not terminated:
				p = multiprocessing.Process(target = decode.decode , args = (self.path,self.savePath,) , name = "Encode Process")
				p.start()
				temp = wx.ProgressDialog('Please wait...', 'Decoding the File....This may take several minutes....\n\t....so sit back and relax....',parent = self,style = wx.PD_APP_MODAL |  wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
				temp.SetSize((450,180))
				while len(multiprocessing.active_children()) != 0:
					time.sleep(0.1)
					if not temp.UpdatePulse("Decoding the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
						p.terminate()
						terminated = True
						self.clear()
						break
				temp.Destroy()
				p.join()
				p.terminate()
				
			if not terminated:
				wx.MessageDialog(self,'File has been created', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
			"""
                        
		elif (not self.pnl1.txt.IsEmpty()) and (FILE_EXT in self.pnl1.txt.GetString(0,self.pnl1.txt.GetLastPosition())) and string != 'None':

                        terminated = False
                        xtime = datetime.now().timetuple()
                        self.savePath = string + "/dCloud_decodedFile_" + `xtime[2]` + "_" + `xtime[1]` + "_" + `xtime[0]`
                        
                        if 'darwin' in sys.platform:
                                p = threading.Thread(name = "Decode", target = decode.decode, args = (self.path,self.savePath,))
                        else:
        			p = multiprocessing.Process(target = decode.decode , args = (self.path,self.savePath,) , name = "Decode Process")
        			
			if not terminated:
				p.start()
                                temp = wx.ProgressDialog('Please wait...', 'Decoding the File....This may take several minutes....\n\t....so sit back and relax....',parent = self,style = wx.PD_APP_MODAL |  wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
				temp.SetSize((450,180))
				if 'darwin' in sys.platform:
                                        while p.isAlive():
                                		time.sleep(0.1)
                                		if not temp.UpdatePulse("Decoding the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
                                			#p.terminate()
                                                        #terminated = True
                                                        wx.MessageDialog(self,'Cannot be stopped.Sorry', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
                                			#break
                                	temp.Destroy()
                                        if not p.isAlive():
                                        	p.join()
                                else:        
        				while len(multiprocessing.active_children()) != 0:
                                                time.sleep(0.1)
        					if not temp.UpdatePulse("Decoding the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
        						p.terminate()
        						terminated = True
        						self.clear()
        						break
               				temp.Destroy()
        				p.join()
        				p.terminate()
			
			if not terminated:
				wx.MessageDialog(self,'File has been created', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
				

		else:
			wx.MessageDialog(self,'Please Select a .dnac file', 'Note!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()

        def discard1(self,e):
                self.pnl1.txt21.Clear()

        def onClear(self,e):
		size = 0
                con = sqlite3.connect(PATH + '/../database/prefs.db')
                with con:
                        cur = con.cursor()
                        WORKSPACE_PATH = cur.execute('SELECT * FROM prefs WHERE id = 8').fetchone()[1]
                        if "linux" in sys.platform:
                                WORKSPACE_PATH = unicodedata.normalize('NFKD', WORKSPACE_PATH).encode('ascii','ignore')
                        if not os.path.isdir(WORKSPACE_PATH + '/.temp'):
                                os.mkdir(WORKSPACE_PATH +  '/.temp')
		
		if "win" in sys.platform and not 'darwin' in sys.platform:
			os.chdir(WORKSPACE_PATH + '\.temp')
			try:
				size += os.path.getsize("dnaString.txt") 
				os.system("del dnaString.txt")
				EXIST_DNASTRING = True
			except OSError:
				EXIST_DNASTRING = False
			try:
				size += os.path.getsize("barcode")
				os.system("del barcode")
				EXIST_BARCODE = True
			except OSError:
				EXIST_BARCODE = False
			try:
				size += os.path.getsize("details.txt")
				os.system("del details.txt")
				EXIST_DETAILS = True
			except OSError:
			      EXIST_DETAILS = False
		
		elif "linux" in sys.platform or 'darwin' in sys.platform:
			os.chdir(WORKSPACE_PATH + '/.temp')
			try:
				size += os.path.getsize("dnaString.txt") 
				os.system("rm dnaString.txt")
				EXIST_DNASTRING = True
			except OSError:
				EXIST_DNASTRING = False
			try:
				size += os.path.getsize("barcode")
				os.system("rm barcode")
				EXIST_BARCODE = True
			except OSError:
				EXIST_BARCODE = False
			try:
				size += os.path.getsize("details.txt")
				os.system("rm details.txt")
				EXIST_DETAILS = True
			except OSError:
			      EXIST_DETAILS = False
		
		os.chdir(PATH)
		"""
		os.chdir(PATH + '\..\database')
		os.system("del dnaBase.db")
		os.chdir(PATH)
		con = lite.connect(PATH + '\..\database\dnaBase.db')
		with con:
			cur = con.cursor()
			cur.execute('DROP TABLE IF EXISTS DNA')
			cur.execute('CREATE TABLE DNA(fileName TEXT NOT NULL,dnaString TEXT NOT NULL)')
                """
		wx.MessageDialog(self,'Temporary Files have been removed\nSpace Freed : '+ str(size/1000000) + " MB" , 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()

#######################################################################
#This are the modules which run when different list items from menu bar are clicked
	def followFB(self,e):
		webbrowser.open(FB_LINK)

	def followTwitter(self,e):
		webbrowser.open(TWITTER_LINK)

	def followQuora(self,e):
		webbrowser.open(QUORA_LINK)
		
	def followYoutube(self,e):
		webbrowser.open(YOUTUBE_LINK)

	def switchWork(self,e):
		panels.workspaceLauncher(None,102,"Switch Workspace!").ShowModal()

	def credits(self,e):
		if "win" in sys.platform and not 'darwin' in sys.platform:
			os.chdir(PATH + '\..\help')
			os.system("start Credits.pdf")
			os.chdir(PATH)
		elif "linux" in sys.platform:
			os.chdir(PATH + '/../help')
			os.system("xdg-open Credits.pdf")
			os.chdir(PATH)
                elif 'darwin' in sys.platform:
                        os.chdir(PATH + '/../help')
                        os.system('open Credits.pdf')
                        os.chdir(PATH)
			

	def productDemo(self,e):
		webbrowser.open(PRODUCT_LINK)

	def productFeedback(self,e):
		webbrowser.open(FEEDBACK_LINK)

        def userManuel(self,e):
		if "win" in sys.platform and not 'darwin' in sys.platform:
			os.chdir(PATH + '\..\help')
			os.system("start UserManual.pdf")
			os.chdir(PATH)
		elif "linux" in sys.platform:
			os.chdir(PATH + '/../help')
			os.system("xdg-open UserManual.pdf")
			os.chdir(PATH)
		elif 'darwin' in sys.platform:
                        os.chdir(PATH + '/../help')
			os.system("open UserManual.pdf")
			os.chdir(PATH)
		
	def exportPdf(self,e):
		fileSelector = wx.FileDialog(self, message="Choose a .dnac file",defaultFile="",style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR )
		if fileSelector.ShowModal() == wx.ID_OK:
			paths = fileSelector.GetPaths()
			if "win" in sys.platform and not 'darwin' in sys.platform:
				filePath = paths[0]
			elif "linux" in sys.platform or 'darwin' in sys.platform:
				filePath = unicodedata.normalize('NFKD', paths[0]).encode('ascii','ignore')
			terminated = False

			if FILE_EXT in filePath:
				locationSelector = wx.FileDialog(self,"Please select location to save your PDF file",style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
				if locationSelector.ShowModal() == wx.ID_OK:
					paths = locationSelector.GetPath()
					if "win" in sys.platform and not 'darwin' in sys.platform:
						savePath = paths
					elif "linux" in sys.platform or 'darwin' in sys.platform:
						savePath = unicodedata.normalize('NFKD', paths).encode('ascii','ignore')
					terminated = False
				else:
					terminated = True
				locationSelector.Destroy()
				del locationSelector

                                if 'darwin' in sys.platform:
                                        #print filePath, savePath
                                        exportToPdf = threading.Thread(name = "Export Thread", target = extraModules.exportToPdf, args = (filePath, savePath,))
                                else:
                			exportToPdf = multiprocessing.Process(target = extraModules.exportToPdf , name = "PDF Exporter" , args = (filePath,savePath))
        			
                                if not terminated:
                                        exportToPdf.start()
                                        temp = wx.ProgressDialog('Exporting to pdf....This may take a while....', 'Please wait...' ,parent = self,style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
                                        temp.SetSize((450,180))
                                        if 'darwin' in sys.platform:
                                                while exportToPdf.isAlive():
                                                        time.sleep(0.1)
                                                        if not temp.UpdatePulse("Exporting the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
                                                                #p.terminate()
                                                                #terminated = True
                                                                wx.MessageDialog(self,'Cannot be stopped.Sorry', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
                                                                #break
                                                temp.Destroy()
                                                if not exportToPdf.isAlive():
                                                        exportToPdf.join()
                                        else:        
                                                while len(multiprocessing.active_children()) != 0:
                                                        time.sleep(0.1)
                                                        if not temp.UpdatePulse("Exporting the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
                                                                exportToPdf.terminate()
                                                                terminated = True
                                                                self.clear()
                                                                break
                                                temp.Destroy()
                                                exportToPdf.join()
                                                exportToPdf.terminate()
			
                                if not terminated:
        				wx.MessageDialog(self,'File has been created', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
				
                                """
				if not terminated:
					exportToPdf = multiprocessing.Process(target = extraModules.exportToPdf , name = "PDF Exporter" , args = (filePath,savePath))
					exportToPdf.start()
					temp = wx.ProgressDialog('Exporting to pdf....This may take a while....', 'Please wait...' ,parent = self,style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
					temp.SetSize((450,180))
					while len(multiprocessing.active_children()) != 0:
						time.sleep(0.1)
						if not temp.UpdatePulse("Exporting the File....This may take several minutes...\n.....so sit back and relax.....")[0]:
							exportToPdf.terminate()
							terminated = True
							break
					temp.Destroy()
					exportToPdf.join()
					exportToPdf.terminate()
			
				if not terminated:
					wx.MessageDialog(self,'PDF created in the desired folder', 'Information!',wx.OK |wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
				"""
			else:
				wx.MessageDialog(self,'Please select a .dnac file', 'Information!',wx.OK |wx.ICON_ERROR | wx.STAY_ON_TOP).ShowModal()
                                
		fileSelector.Destroy()
		del fileSelector

	def exportLatex(self,e):
		fileSelector = wx.FileDialog(self, message="Choose a .dnac file",defaultFile="",style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR )
		if fileSelector.ShowModal() == wx.ID_OK:
			paths = fileSelector.GetPaths()
			if "win" in sys.platform and not 'darwin' in sys.platform:
				filePath = paths[0]
			elif "linux" in sys.platform or 'darwin' in sys.platform:
				filePath = unicodedata.normalize('NFKD', paths[0]).encode('ascii','ignore')
			terminated = False

			if FILE_EXT in filePath:
				locationSelector = wx.FileDialog(self,"Please select location to save your Latex file",style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
				if locationSelector.ShowModal() == wx.ID_OK:
					paths = locationSelector.GetPath()
					if "win" in sys.platform and not 'darwin' in sys.platform:
						savePath = paths
					elif "linux" in sys.platform or 'darwin' in sys.platform:
						savePath = unicodedata.normalize('NFKD', paths).encode('ascii','ignore')
					terminated = False
				else:
					terminated = True
				locationSelector.Destroy()
				del locationSelector

                                if 'darwin' in sys.platform:
                                        exportToLatex = threading.Thread(name = "Export Thread", target = extraModules.exportToLatex, args = (filePath, savePath,))
                                else:
                                        exportToLatex = multiprocessing.Process(target = extraModules.exportToLatex , name = "Latex Exporter" , args = (filePath,savePath))
                                        
                                if not terminated:
                                        exportToLatex.start()
                                        temp = wx.ProgressDialog('Exporting to latex file....This may take a while....', 'Please wait...' ,parent = self,style = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
                                        temp.SetSize((450,180))
                                        if 'darwin' in sys.platform:
                                                while exportToLatex.isAlive():
                                                        time.sleep(0.1)
                                                        if not temp.UpdatePulse("Exporting the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
                                                                #p.terminate()
                                                                #terminated = True
                                                                wx.MessageDialog(self,'Cannot be stopped.Sorry', 'Information!',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
                                                                #break
                                                temp.Destroy()
                                                if not exportToLatex.isAlive():
                                                        exportToLatex.join()
                                        else:        
                                                while len(multiprocessing.active_children()) != 0:
                                                        time.sleep(0.1)
                                                        if not temp.UpdatePulse("Exporting the File....This may take several minutes...\n\tso sit back and relax.....")[0]:
                                                                exportToLatex.terminate()
                                                                terminated = True
                                                                self.clear()
                                                                break
                                                temp.Destroy()
                                                exportToLatex.join()
                                                exportToLatex.terminate()

        			"""
				if not terminated:
					exportToLatex = multiprocessing.Process(target = extraModules.exportToLatex , name = "Latex Exporter" , args = (filePath,savePath))
					exportToLatex.start()
					temp = wx.ProgressDialog('Exporting to latex file....This may take a while....', 'Please wait...',parent = self, style = 	wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
					temp.SetSize((450,180))
					while len(multiprocessing.active_children()) != 0:
						time.sleep(0.1)
						if not temp.UpdatePulse("Exporting to latex file....This may take several minutes...\n.....so sit back and relax.....")[0]:
							exportToLatex.terminate()
							terminated = True
							break
					temp.Destroy()
					exportToLatex.join()
					exportToLatex.terminate()
                                
				if not terminated:
					wx.MessageDialog(self,'Latex File created in the desired folder', 'Information!',wx.OK |wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
				"""
			else:
				wx.MessageDialog(self,'Please select a .dnac file', 'Information!',wx.OK |wx.ICON_ERROR | wx.STAY_ON_TOP).ShowModal()
		fileSelector.Destroy()
		del fileSelector
		
	def exportList(self,e):
		"""
		files = []
		print PATH
		con = lite.connect(PATH + '/../database/dnaBase.db')
		with con:
			cur = con.cursor()
			for i in cur.execute('SELECT * FROM DNA'):
				files.append(str(i[0]))
		ChoiceSelected = wx.SingleChoiceDialog(self,"Please select file you like to export?","Export",files,wx.CHOICEDLG_STYLE)
		result = ChoiceSelected.ShowModal()
		ChoiceSelected.Centre(wx.BOTH)
		if result == wx.ID_OK:
			ChoiceSelected.Destroy()
			for i in cur.execute('SELECT * FROM DNA'):
				if ChoiceSelected.GetStringSelection() == i[0]:
					p = multiprocessing.Process(target = extraModules.writeListToCsv , args = (i[1],PATH + "/../CSVFiles"))
					p.start()
					temp = wx.ProgressDialog('Exporting the List....This may take a while....', 'Please wait...',style = wx.PD_APP_MODAL)
					temp.SetSize((400,100))
					while len(multiprocessing.active_children()) != 0:
						time.sleep(0.5)
						temp.Pulse("Exporting the list....")
					temp.Destroy()
					wx.MessageDialog(self,'Your List is exported', 'Congratulations',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
					break
			del ChoiceSelected
		else:
			ChoiceSelected.Destroy()
		"""
                wx.MessageDialog(self,'This feature is yet to be added please bear with us', 'Sorry',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()

	def importList(self,e):
                """
		print "Importing..."
		fileSelector = wx.FileDialog(self, message="Choose a file",defaultFile="",style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR )
		if fileSelector.ShowModal() == wx.ID_OK:
			paths = fileSelector.GetPaths()
			fileSelector.Destroy()
			path = paths[0]
			del fileSelector
			p = multiprocessing.Process(target = extraModules.readListFromCsv , args = (path,PATH + '/../decodedFiles'))
			p.start()
			temp = wx.ProgressDialog('Importing the List....This may take a while....', 'Please wait...',style = wx.PD_APP_MODAL)
			temp.SetSize((400,100))
			while len(multiprocessing.active_children()) != 0:
				time.sleep(0.5)
				temp.Pulse("Importing the List....")
			temp.Destroy()
			wx.MessageDialog(self,'Your File is created in the folder from the string imported', 'Congratulations',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
		else:
			fileSelector.Destroy()
		"""
                wx.MessageDialog(self,'This feature is yet to be added please bear with us', 'Sorry',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
        """
	def exportString(self,e):
                files = []
                con = lite.connect(PATH + '/../database/dnaBase.db')
                with con:
                        cur = con.cursor()
                        for i in cur.execute('SELECT * FROM DNA'):
                                files.append(str(i[0]))
		ChoiceSelected = wx.SingleChoiceDialog(self,"Please select file you like to export?","Export",files,wx.CHOICEDLG_STYLE)
		result = ChoiceSelected.ShowModal()
		ChoiceSelected.Centre(wx.BOTH)
		if result == wx.ID_OK:
			ChoiceSelected.Destroy()
			for i in cur.execute('SELECT * FROM DNA'):
				if ChoiceSelected.GetStringSelection() == i[0]:
					p = multiprocessing.Process(target = extraModules.writeStringToCsv , args = (i[1],PATH + '/../CSVFiles') , name = "Export Process")
					p.start()
					temp = wx.ProgressDialog('Exporting the String....This may take a while....', 'Please wait...',style = wx.PD_APP_MODAL)
					temp.SetSize((400,100))
					while len(multiprocessing.active_children()) != 0:
						time.sleep(0.5)
						temp.Pulse("Exporting the String....This may take a while....")
					temp.Destroy()
					wx.MessageDialog(self,'Your String is exported', 'Congratulations',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
					break
			del ChoiceSelected
        	else:
                	ChoiceSelected.Destroy()

	
	def importString(self,e):
		print "Importing..."
		fileSelector = wx.FileDialog(self, message="Choose a file",defaultFile="",style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR )
		if fileSelector.ShowModal() == wx.ID_OK:
			paths = fileSelector.GetPaths()
			fileSelector.Destroy()
			path = unicodedata.normalize('NFKD', paths[0]).encode('ascii','ignore')
			del fileSelector
			p = multiprocessing.Process(target = extraModules.readStringFromCsv , args = (path,PATH + '/../decodedFiles'))
			p.start()
			temp = wx.ProgressDialog('Importing the String....This may take a while....', 'Please wait...',style = wx.PD_APP_MODAL)
			temp.SetSize((400,100))
			while len(multiprocessing.active_children()) != 0:
				time.sleep(0.5)
				temp.Pulse("Importing the String....")
			temp.Destroy()
			wx.MessageDialog(self,'Your File is created in the folder from the string imported', 'Congratulations',wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
		else:
			fileSelector.Destroy()
	"""

#Show a confirmation dialog box if the user wants to quit or not and for that show modal shows box 
	def OnQuit(self,item):        
	    quitMessageBox = wx.MessageDialog(self,"Are you sure you want to Quit??","Quitting the Application",wx.YES | wx.NO | wx.ICON_EXCLAMATION)
	    result = quitMessageBox.ShowModal();
	    if result == wx.ID_YES:
		super(MyFrame,self).Destroy()
		sys.exit()
	    elif result == wx.ID_NO:
		quitMessageBox.Destroy()
	    
	def newMenuItemEncode(self,e):
		if self.pnl1.IsShown():
			self.pnl1.Hide()
			self.pnl.Show()
			self.clear()
			self.Layout()
			self.pnl.Refresh()
			self.bindEncodeItems()
			gc.collect()
		elif not (self.pnl1.IsShown() or self.pnl.IsShown()):
			self.pnl.Show()
			self.clear()
			self.Layout()
			self.pnl.Refresh()
			self.bindEncodeItems()
			gc.collect()
		else:
			wx.MessageDialog(self,"You are already on the Encode Page!","Note!",wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()

	def newMenuItemDecode(self,e):
		if self.pnl.IsShown():
			self.pnl.Hide()
			self.pnl1.Show()
			self.Layout()
			self.bindDecodeItems()
			self.pnl1.Refresh()
			gc.collect()
		elif not (self.pnl1.IsShown() or self.pnl.IsShown()):
			self.pnl1.Show()
			self.clear()
			self.Layout()
			self.pnl.Refresh()
			self.bindEncodeItems()
			gc.collect()
		else:
			wx.MessageDialog(self,"You are already on the Decode Page!","Note!",wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
                        
	def aboutUs(self,e):
		info = wx.AboutDialogInfo()
		if "win" in sys.platform and not 'darwin' in sys.platform:
			info.SetIcon(wx.Icon(PATH + '\..\icons\DNAicon.png', wx.BITMAP_TYPE_PNG))
		elif "linux" in sys.platform or 'darwin' in sys.platform:
			info.SetIcon(wx.Icon(PATH + '/../icons/DNAicon.png', wx.BITMAP_TYPE_PNG))  
		info.SetName(NAME)
		info.SetVersion(VERSION)
		info.SetDescription(ABOUT_DESCRIPTION)
		info.SetCopyright(ABOUT_COPYRIGHT)
		info.SetWebSite(OFFICIAL_WEBSITE)
		
		info.SetLicence(DETAILED_LICENSE)
		info.AddDeveloper(KEY_DEVELOPER)
		info.AddArtist(ICON_ARTIST)
		info.AddArtist(ICON_IDEA)
		wx.AboutBox(info)

	def settings(self,e):
	      p = panels.Preferences(None,0,"Details").ShowModal()

	      """
	      self.qrText = ""
	      if "win" in sys.platform:
			con = sqlite3.connect(PATH + '\..\database\prefs.db')
		elif "linux" in sys.platform:
			con = sqlite3.connect(PATH + '/../database/prefs.db')
	      with con:
			self.qrText = ""
			cur = con.cursor()
			for i in cur.execute('SELECT * FROM prefs WHERE id < 4'):
				self.qrText = self.qrText + i[1] + "\n"
	      #self.onUseQrcode(self.qrText)
	      """

	def memEstimator(self,e):
		gc.collect()
		panels.memEstimator(None,103,"Approximate the Values").ShowModal()
		
	def estimator(self,e):
		gc.collect()
		panels.estimator(None,103,"Approximate the Values").ShowModal()

	def exportBarcode(self,e):
                con = sqlite3.connect(PATH + '/../database/prefs.db')
                with con:
                        cur = con.cursor()
                        WORKSPACE_PATH = cur.execute('SELECT * FROM prefs WHERE id = 8').fetchone()[1]
                        if "linux" in sys.platform:
                                WORKSPACE_PATH = unicodedata.normalize('NFKD', WORKSPACE_PATH).encode('ascii','ignore')
                        if not os.path.isdir(WORKSPACE_PATH + '/barcode'):
                                os.mkdir(WORKSPACE_PATH +  '/barcode')
                                wx.MessageDialog(self,'Software cannot find barcode please go to prefrences and generate a barcode!', 'Information!',wx.OK |wx.ICON_ERROR | wx.STAY_ON_TOP).ShowModal()
                                return
                        
                fileSelector = wx.FileDialog(self, message="Choose a location to save barcode",style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if fileSelector.ShowModal() == wx.ID_OK:
			paths = fileSelector.GetPaths()
			if "win" in sys.platform and not 'darwin' in sys.platform:
				barcodeFile = file(paths[0] + ".png","wb")
				barcodeFile.write(open(WORKSPACE_PATH + '\\barcode\\barcode.png',"rb").read())
			elif "linux" in sys.platform or 'darwin'in sys.platform:
				paths = unicodedata.normalize('NFKD', paths[0]).encode('ascii','ignore')
				barcodeFile = file(paths + ".png","wb")
				barcodeFile.write(open(WORKSPACE_PATH + '/barcode/barcode.png',"rb").read())
			barcodeFile.close()
			wx.MessageDialog(self,'Last generated barcode Saved to specified location', 'Information!',wx.OK |wx.ICON_INFORMATION | wx.STAY_ON_TOP).ShowModal()
                fileSelector.Destroy()
		del fileSelector

#######################################################################
#This functions are binding the buttons whenever views are changed

        def bindEncodeItems(self):
                #self.pnl.but9.Bind(wx.EVT_BUTTON,self.viewString)
                #self.pnl.but10.Bind(wx.EVT_BUTTON,self.viewList)
                self.pnl.butChoose.Bind(wx.EVT_BUTTON,self.onChoose)
                self.pnl.saveBut.Bind(wx.EVT_BUTTON,self.save)
                self.pnl.discardBut.Bind(wx.EVT_BUTTON,self.discard)
                #self.pnl.clearDB.Bind(wx.EVT_BUTTON,self.onClear)

        def bindDecodeItems(self):
		self.pnl1.butChoose.Bind(wx.EVT_BUTTON,self.onChoose)
		self.pnl1.decodeBut.Bind(wx.EVT_BUTTON,self.decodeBut1)
		self.pnl1.resetBut.Bind(wx.EVT_BUTTON,self.discard1)
		self.pnl1.decodeBut1.Bind(wx.EVT_BUTTON,self.decodeBut2)

#Splash Screen Class this is used to make the DNA Splash Screen
class MySplashScreen(wx.SplashScreen):
    def OnSplashScreenExit(self,e):
        self.Hide();
        frame = MyFrame(None)
                
    def __init__(self,parent=None):
        if "linux" in sys.platform or "darwin" in sys.platform:
	  bmp = wx.Bitmap(PATH + '/../icons/DNA.png', wx.BITMAP_TYPE_PNG)
        elif "win" in sys.platform and not 'darwin' in sys.platform:
	  bmp = wx.Bitmap(PATH + '\..\icons\DNA.png', wx.BITMAP_TYPE_PNG)                
        wx.SplashScreen.__init__(self,bmp,wx.SPLASH_CENTER_ON_SCREEN | wx.SPLASH_TIMEOUT,SPLASH_TIMEOUT,parent)
        self.Bind(wx.EVT_CLOSE,self.OnSplashScreenExit)
        
###############################################################

if __name__ == "__main__":
        app = wx.App()
        if not "darwin" in sys.platform:
                multiprocessing.freeze_support()
        Splash = MySplashScreen()
        app.MainLoop()
        if not 'darwin' in sys.platform:
                sys.exit(0)