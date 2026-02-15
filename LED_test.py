'''This code tests a simple LED circuit connected to GPIO pin
   The LED blinks 5 times for the frequency in seconds
   Example terminal command: python LED_test.py 21 1'''

import sys
import time
import RPi.GPIO as GPIO

redLED = int(sys.argv[1]) #First argument is the GPIO pin the LED cathode is connected to
freq = int(sys.argv[2]) #Second argument is the frequency at which the LED will blink
GPIO.setmode(GPIO.BCM) #Specifies the number of the GPIO pin
GPIO.setup(redLED, GPIO.OUT) #Set LED to GPIO out pin
GPIO.setwarnings(False) #Don't generate warnings

for i in range(5): #Blinks LED on and off for the set frequency 5 times in a row
    GPIO.output(redLED, GPIO.LOW)
    time.sleep(freq)
    GPIO.output(redLED, GPIO.HIGH)
    time.sleep(freq)
    
GPIO.cleanup() #Shut down GPIO