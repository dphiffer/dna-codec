"""
#########################################################################
Author: Shalin Shah
Project: DNA Cloud
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Date: 28 July 2013
Website: www.guptalab.org/dnacloud
This module is used to create a bracode.
#########################################################################
"""
import sys
import barcode
from barcode import generate
from barcode.writer import ImageWriter
from PIL import PngImagePlugin
#if 'darwin' in sys.platform:
#	from PIL import Image
#	from PIL import ImageFont
#	from PIL import ImageDraw

def generate(details,path):
	  EAN = barcode.get_barcode_class('code128')
	  ean = EAN(details, writer=ImageWriter())
	  barcodePic = ean.save(path + 'barcode')

"""
This is the code to generate QR Code just write it in Main Frame.py and ready to go
######################################################################
#This are the 2 functions which generate QR code
self.photo_max_size = 240
	def onUseQrcode(self, text):
	    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10)
	    qr.add_data(text)
	    qr.make(fit=True)
	    x = qr.make_image()
 
	    img_file = open(PATH + '/../icons/qr.jpg', 'wb')
	    x.save(img_file, 'JPEG')
	    img_file.close()
	    self.showQRCode(PATH + '/../icons/qr.jpg')
		
		
	def showQRCode(self, filepath):
		img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
		# scale the image, preserving the aspect ratio
		W = img.GetWidth()
		H = img.GetHeight()
		if W > H:
			NewW = self.photo_max_size
			NewH = self.photo_max_size * H / W
		else:
			NewH = self.photo_max_size
			NewW = self.photo_max_size * W / H
		img = img.Scale(NewW,NewH)
		if self.pnl.IsShown():
			self.pnl.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
		elif self.pnl1.IsShown():
			self.pnl1.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
		self.Refresh()

###############################################################
"""
