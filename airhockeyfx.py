import selectormodule as sm
import cv2
import numpy as np 


def AirHockey():

	#Initializes game,camera, and paddle Tracker
	createVelocityAdjuster()
	cap=cv2.VideoCapture(0)
	masker = sm.ColorSelector()


	#



def playGame(self):
	#in x,y
	xpos,ypos=[1,1]
	paddleX,paddleY = (0,0)
	xdrx,ydrx=[10,1]

	while True:

		# Reads in camera data and makes mask from color selection
		_ret, image = self.cap.read()
		image = cv2.flip(image,1)
		self.masker.loadImage(image)
		mask1 = self.masker.getMask()

		#finds the largest continuos region of specified color
		(cnts, _) = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if len(cnts) != 0: 	
			maxRegion=self.findLargestContour(cnts)
			
		  	#Shows largest region
		 	#maxRegionImage = np.zeros((mask1.shape[:2]),dtype = 'uint8')
			#cv2.drawContours(paddle, [maxRegion], -1, 255, -1)
			#cv2.imshow('maxRegion',maxRegionImage)


			#Stores the center of the largest region
			((paddleX, paddleY), radius) = cv2.minEnclosingCircle(maxRegion)
		

		v = cv2.getTrackbarPos('Velocity', 'game')
		velocity=[xdrx*v,ydrx*v]
		rows,columns = mask1.shape[:2]


		airHockeyField = np.zeros((rows,columns), dtype = "uint8")
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














def createVelocityAdjuster():
	cv2.namedWindow('game')
	#Assigns the velocity trackbar to game window
	cv2.createTrackbar('Velocity', 'game',1,100,nothing) 

def nothing(x):
	pass