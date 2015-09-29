# import the necessary packages
import numpy as np
import argparse
import cv2


class ColorSelector:
	"""A class that serves as an eyedropper mask tool. Allows user to 
	select a color range dand then creates a mask based on that"""

	def __init__(self):

		self.column = 0
		self.row = 0
		self.color = [0,0,0]
		self.lowercolor =None
		self.uppercolor = None
		self.shifter = np.array([10,10,10])
		self.colorwheel = np.zeros((300,300,3), dtype = "uint8")
		self.setWindow()
		self.cap = cv2.VideoCapture(0)
		self.image = None

	def loadImage(self,image):
		self.image = image


	# Creates an eyedropper tool and allows you to select the high and low 
	# values for the color range
	def getColor(self,event, x, y, flags, param):
		if event == cv2.EVENT_MOUSEMOVE:
			(self.column,self.row) = (x,y)
			#print 'row %i column %i' %(row,column)
			self.color = np.array(self.image[self.row,self.column])
			#print 'color: ', color
			self.colorwheel[:,:,:]= self.color
		
		elif event == cv2.EVENT_LBUTTONDOWN:
			confirm = raw_input('1 for Lower Color Range, 2 for Upper Color Range: ')
			if confirm == '1':
				self.lowercolor = self.color-self.shifter
				print 'lowercolor', self.lowercolor
			if confirm == '2':
				self.uppercolor = self.color+self.shifter
				print "uppercolor: ", self.uppercolor



	def setWindow(self):
		cv2.namedWindow("image")
		cv2.setMouseCallback("image", self.getColor)
		#global colorwheel 
		#colorwheel = np.zeros((300,300,3), dtype = "uint8")

			

	# Creates a mask out of the image and the color range
	def getMask(self):

		cv2.imshow('color', self.colorwheel)
		h,w=self.image.shape[:2]

		# resizes selector video stream
		self.image = cv2.resize(self.image,(int(w*.8),int(h*.8)), interpolation = cv2.INTER_AREA)
		cv2.imshow('image',self.image)
		mask = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)

		if (self.lowercolor is not None and self.uppercolor is not None):
 
			#creates the mask using the inRange function
			mask = cv2.inRange(self.image, self.lowercolor, self.uppercolor)

			#performs some dilations and erosions to regularize mask
			kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
			kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
			mask = cv2.erode(mask, kernel, iterations = 4)
			mask = cv2.dilate(mask, kernel2, iterations = 4)
			mask = cv2.medianBlur(mask,11)

		cv2.imshow('mask',mask)
		return mask
		
