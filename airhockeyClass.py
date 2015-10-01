import selectormodule as sm
import cv2
import numpy as np 




class AirHockey:

	def __init__(self):
		self.createVelocityAdjuster()
		self.cap = cv2.VideoCapture(0)
		self.masker = sm.ColorSelector()
		self.playGame()



	def playGame(self):
		#in x,y
		xpos,ypos=[1,1]
		paddleX,paddleY = (0,0)
		xdrx,ydrx=[1,1]

		while True:

			# Reads in camera data and makes mask from color selection
			_ret, image = self.cap.read()
			image = cv2.flip(image,1)
			self.masker.loadImage(image)
			mask1 = self.masker.getMask()
			rows,columns = mask1.shape[:2]

			#Creates field the same size as the mask frame
			airHockeyField = np.zeros((rows,columns), dtype = "uint8")

			#finds the largest continuos region of specified color
			(cnts, _) = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			if len(cnts) != 0: 	
				maxRegion=self.findLargestContour(cnts)
				
			  	
				#Stores the center of the largest region
				((paddleX, paddleY), radius) = cv2.minEnclosingCircle(maxRegion)
			

			v = cv2.getTrackbarPos('Velocity', 'game')
			velocity=[xdrx*v,ydrx*v]


			xpos = int(xpos+velocity[0])
			ypos = int(ypos+velocity[1])
		
			#Makes sure the ball's location doesn't get moved past the boundaries of the frame
			xpos = 0 if xpos < 0 else columns if xpos > columns else xpos
			ypos = 0 if ypos < 0 else rows if ypos > rows else ypos

			
			paddleX = columns-paddleX

			#Draws the puck and paddle circles
			cv2.circle(airHockeyField,(xpos,ypos), 10, 255,-1)
			cv2.circle(airHockeyField,(int(paddleX),int(paddleY)), 30, 120,-1)


			#Reflects the ball if it intersects edges or the puck
			if xpos <= 0 or xpos >= columns or airHockeyField[ypos-1,xpos-1] == 120:
				xdrx=-1*xdrx
			if ypos <= 0 or ypos >= rows:
				ydrx=-1*ydrx




			cv2.imshow('game', airHockeyField)
			if cv2.waitKey(10)==27:
				break



	@staticmethod
	def findLargestContour(contours):
		max_area = 0
		for i in range(len(contours)):
			cnt=contours[i]
			area = cv2.contourArea(cnt)
			if(area>max_area):
				max_area=area
				maxIndex=i
		return contours[maxIndex]



	# Creates Velocity adjuster for ping pong ball
	def createVelocityAdjuster(self):
		cv2.namedWindow('game')
		#Assigns the velocity trackbar to game window
		cv2.createTrackbar('Velocity', 'game',1,100,self.nothing) 


	#The createTrackbar needs a method, so nothing() is a placeholder
	@staticmethod
	def nothing(x):
		pass

AirHockey()
