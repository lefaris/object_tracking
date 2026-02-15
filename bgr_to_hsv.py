'''This code converts a target BGR value to a trackable HSV value for OpenCV
   It reads in a BGR value and outputs an HSV range for object tracking
   Example terminal command: python bgr_to_hsv.py 180 0 41'''

import sys
import numpy as np
import cv2

blue = sys.argv[1] #The first argument is the blue value of the target object color
green = sys.argv[2] #The second argument is the green value of the target object color
red = sys.argv[3] #The third argument is the red value of the target object color

color = np.uint8([[[blue, green, red]]]) #Turns the input arguments into an 8-bit unsigned integer
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV) #Converts the BGR values into HSV values
hue = hsv_color[0][0][0] #Set to hue to three HSV channel values

print("HSV range is between [" + str(hue-10) + ", 100, 100] and [" + str(hue + 10) + ", 255, 255]") #Print range