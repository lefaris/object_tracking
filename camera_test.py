'''This code tests that the Raspberry Pi Camera Module 3 is working
   It saves BGR and grayscale images in a specified directory
   Example terminal command: python camera_test.py'''

import cv2
import os
import time
from picamera2 import Picamera2

cv2.startWindowThread() #Start window for the camera
picam2 = Picamera2() #Assign the pi camera to the Picamera2 library
picam2.start() #Start up the camera

output_dir = "Lab1" #Specify folder to save images to
os.makedirs(output_dir,exist_ok=True) #Makes the directory if it doesn't exist

while True: #Continue to run until stopped
    im_bgr = picam2.capture_array() #Capture an image and assign it to variable im_bgr
    im = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY) #Convert captured BGR image to grayscale
    timestamp = int(time.time()) #Returns an integer of time in seconds
    
    filename = os.path.join(output_dir, f"rgb_{timestamp}.jpg") #Sets filename to bgr + timestamp in the specified directory
    cv2.imwrite(filename, im) #Saves the file
    gray_filename = os.path.join(output_dir, f"gray_{timestamp}.jpg")
    cv2.imwrite(gray_filename, gray)
    
    cv2.imshow("Camera", im) #Shows the image in the window
    cv2.imshow("Camera", gray)
