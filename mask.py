'''OpenCV generates a mask of the specified object color of interest
   It reads in an image containing the target and the HSV range for
   that specific color and creates a binary mask output
   Example terminal command: python mask.py'''

import numpy as np
import cv2

img_bgr = cv2.imread('solo_cup.jpg', 1) #Specify the image input and 1 defaults to BGR
img_bgr = cv2.resize(img_bgr, (0,0), fx=0.2, fy=0.2) #Shrink image to 20% in each axis for faster conversion
img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV) #Generate HSV image

lower_range = np.array([117, 100, 100], dtype=np.uint8) #Manually set HSV range values
upper_range = np.array([137, 255, 255], dtype=np.uint8)

mask = cv2.inRange(hsv, lower_range, upper_range) #Generate the mask
cv2.imshow('Mask', mask) #Show the mask
cv2.imshow('RGB', img) #Show the corresponding RGB image
cv2.imshow('HSV', hsv) #Show the corresponding HSV image

while(1):
    k = cv2.waitKey(0)
    if (k == 27):
        break
    
cv2.destroyAllWindows()
