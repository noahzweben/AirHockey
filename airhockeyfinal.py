from selectormodule import *
import cv2
import numpy as np 


# Creates Velocity adjuster for ping pong ball
cv2.namedWindow('game')
cv2.createTrackbar('Velocity', 'game',1,100,nothing) #Assigns the velocity trackbar to game window
def nothing(x):
	pass

#in x,y
position = np.array([1,1])
paddleX,paddleY = (0,0)

cap = cv2.VideoCapture(0)

masker = ColorSelector()
while True:
	_ret, image = cap.read()
	image = cv2.flip(image,1)
	masker.loadImage(image)
	#Find paddle and make circle from it
	mask1 = masker.getMask()
	(cnts, _) = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	max_area=0
	#print 'x contours', len(cnts)
	if len(cnts) != 0: 	
		for i in range(len(cnts)):
	            cnt=cnts[i]
	            area = cv2.contourArea(cnt)
	            if(area>max_area):
	                max_area=area
	                ci=i
	  	cnt=cnts[ci]

	  	paddle = np.zeros((mask1.shape[:2]),dtype = 'uint8')
		cv2.drawContours(paddle, [cnt], -1, 255, -1)
		cv2.imshow('paddle',paddle)


		((paddleX, paddleY), radius) = cv2.minEnclosingCircle(cnt)


	#HOCKEY STUFF	
	v = cv2.getTrackbarPos('Velocity', 'game')
	velocity=[xdrx*v,ydrx*v]
	rows,columns = mask1.shape[:2]
	field = np.zeros((rows,columns), dtype = "uint8")
	xpos = int(position[0]+velocity[0])
	ypos = int(position[1]+velocity[1])
	xpos = 0 if xpos < 0 else columns if xpos > columns else xpos
	ypos = 0 if ypos < 0 else rows if ypos > rows else ypos
	position = (xpos, ypos) 
	paddleX = columns-paddleX
	cv2.circle(field,tuple(position), 10, 255,-1)
	cv2.circle(field,(int(paddleX),int(paddleY)), 30, 120,-1)


	if xpos <= 0 or xpos >= columns or field[ypos-1,xpos-1] == 120:
		xdrx= -1*xdrx
	if ypos <= 0 or ypos >= rows:
		ydrx= -1*ydrx



	cv2.imshow('game', field)



	if cv2.waitKey(10)==27:
		break
		