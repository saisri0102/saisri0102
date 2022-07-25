
from collections import deque					# import the necessary packages import numpy as np import argparse import imutils import cv2 import serial import time x=0 #initilize x,y,r coordinates of the ball to zero y=0 r=0 ap = argparse.ArgumentParser() 					#We are creating a buffer to store the tracked points ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size") #buffer size to store last 64 frames args = vars(ap.parse_args()) HSV_Lower = (10,116,210) # define the lower and upper boundaries of the "HSV color" HSV_Upper = (79,255,255) # ball in the HSV color space, then initialize the pts = deque(maxlen=args["buffer"]) # list of tracked points camera = cv2.VideoCapture(0) #initialize the primary camera while True: 	ret, frame = camera.read() # grab the current frame 	cv2.circle(frame,(325,215), 2, (0,255,0), -1) 	 	#centre of the frame marked in green dot 	 	frame = imutils.resize(frame,width=600,height=400) # resize the frame to size 600X400 	blurred = cv2.GaussianBlur(frame, (11, 11), 0) # blur the frame to smoothen it, 	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert it to the HSV color space 	mask = cv2.inRange(hsv, HSV_Lower, HSV_Upper) # construct a mask for the separating color from background 	cv2.imshow("mask",mask) # display mask 	mask = cv2.erode(mask, None, iterations=2) #Perform a series of dilations and erosions to 	mask = cv2.dilate(mask, None, iterations=2) #remove any smallblobs left in the mask # find contours in the mask and initialize the current 								# (x, y) center of the ball 	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] center = None #initialize the center of ball (x,y) to none 	if len(cnts) > 0:				 # only proceed if at least one contour was found 		c = max(cnts, key=cv2.contourArea) # find the largest contour in the mask, then use 		((x, y), radius) = cv2.minEnclosingCircle(c) # it to compute the minimum enclosing circle and 		M = cv2.moments(c) # find the centroid 		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) 		if radius > 0:					# only proceed if the radius meets a minimum size 			# draw the circle and centroid on the frame, 			# then update the list of tracked points 			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2) 			cv2.circle(frame, center, 5, (0, 0, 255), -1) #centre of the ball 			x=int(x) 			y=int(y) 			r=int(radius) 			print x,y,r 			output = "X{0:d}Y{1:d}Z{2:d}".format(x,y,r) 	 	cv2.imshow("Frame", frame)				# show the frame to our screen 	key = cv2.waitKey(1) & 0xFF 	if key == ord("q"): # if the 'q' key is pressed, stop the loop 		break camera.release() #release the camera cv2.destroyAllWindows() #destroy all frames