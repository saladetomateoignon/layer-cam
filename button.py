#Mostly taken from here: http://www.stuffaboutcode.com/2013/09/raspberry-pi-gps-setup-and-python.html
# Author is Martin O'Hanlon

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)

import time
import os

prev_input= 1
while True:
    button_input = GPIO.input(17)
    if ((not prev_input) and button_input):
    	os.system("sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock")
        os.system("sudo python /home/pi/Desktop/Python/GPSandAPI/gpsandapi_panoramio_raspi.py")
    prev_input = button_input
    time.sleep(0.05)
