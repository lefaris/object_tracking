'''Tracks an object with a specified color of interest. Instead of a
   continuous line following the object, a dot is displayed in the center
   of the object and the red LED turns on when the object is in frame
   Adapted from the original code developed by Adrian Rosebrock
   Visit original post: https://www.pyimagesearch.com/2016/05/09/opencv-rpi-gpio-and-gpio-zero-on-the-raspberry-pi/
   Example terminal command: python tracking_LED.py'''

from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import RPi.GPIO as GPIO
from picamera2 import Picamera2

cv2.startWindowThread()
picam2 = Picamera2()
picam2.start()

redLED = 21
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(redLED, GPIO.OUT)

colorLower = (117, 100, 100) 
colorUpper = (137, 255, 255) 

GPIO.output(redLED, GPIO.LOW)
ledOn = False
while True: #Loop through images
    frame_bgr = picam2.capture_array()
    frame_bgr = imutils.resize(frame_bgr, width=500) #Resize image
    frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB) #Adding here to try to correct colors
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV) #Adding here to try to correct colors
    mask = cv2.inRange(hsv, colorLower, colorUpper) #Generate initial mask
    mask = cv2.erode(mask, None, iterations=2) #Erode to remove small blob errors that are not object
    mask = cv2.dilate(mask, None, iterations=2) #Dilate to keep original object of interest size

    #Look for contours in mask and set center to object center
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
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
            if not ledOn: #Turn LED on
                GPIO.output(redLED, GPIO.HIGH)
                ledOn = True

    elif ledOn: #Turn LED off
        GPIO.output(redLED, GPIO.LOW)
        ledOn = False

    cv2.imshow("Frame", frame) #Show the image with the object being tracked
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

GPIO.cleanup() #Clean GPIO
cv2.destroyAllWindows()
