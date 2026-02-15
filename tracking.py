'''This code tracks any object with the specified color of interest
   Adapted from ball tracking code developed by Adrian Rosebrock
   Visit original post: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
   Example terminal command: python tracking.py'''

from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from picamera2 import Picamera2

cv2.startWindowThread()
picam2 = Picamera2()
picam2.start()

colorLower = (117, 100, 100)
colorUpper = (137, 255, 255)
pts = deque(maxlen=64)

while True:
    frame_bgr = picam2.capture_array()
    frame_bgr = imutils.resize(frame_bgr, width=600) #Resize the image
    frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB) #Adding here to try to correct colors
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV) #Adding here to try to correct colors
    mask = cv2.inRange(hsv, colorLower, colorUpper) #Generate initial mask
    mask = cv2.erode(mask, None, iterations=2) #Erode to remove small blob errors that are not object
    mask = cv2.dilate(mask, None, iterations=2) #Dilate to keep original object of interest size
    
    #Look for contours in mask and set center to object center
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
 
    if len(cnts) > 0: #If contour exists
        #Use largest contour to generate enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        if radius > 10: #If radius is at least 11 pixels, proceed
            #Draw the circle and centroid, updating the tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
    pts.appendleft(center) #Update the points
    for i in range(1, len(pts)): #For all tracked points
        if pts[i - 1] is None or pts[i] is None: #Ignore empty points
            continue
        thickness = int(np.sqrt(64 / float(i + 1)) * 2.5) #Generate the continuous line thickness
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness) #Draw connecting line

    cv2.imshow("Frame", frame) #Show the image with the object being tracked
    key = cv2.waitKey(1) & 0xFF
 
    if key == ord("q"):
        break

picam2.release() #Stop camera
cv2.destroyAllWindows()
