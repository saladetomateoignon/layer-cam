#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
 
import os
from gps import *
from time import *
import time
import threading
import sys

import urllib2
import urllib
import random
import json
from pprint import pprint

gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
          #It may take a second or two to get good data 
    while True:
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
      data = {}
      data['set'] = 'full' #public
      data['from'] = '0'
      data['to'] = '10'
      data['minx'] = gpsd.fix.longitude -0.001
      data['maxx'] = gpsd.fix.longitude +0.001
      data['miny'] = gpsd.fix.latitude -0.001
      data['maxy'] = gpsd.fix.latitude +0.001
      data['size'] = 'original'
      data['mapfilter'] = 'true'
      url_values = urllib.urlencode(data)
      #print url_values  # The order may differ. 

      url = 'http://www.panoramio.com/map/get_panoramas.php'
      full_url = url + '?' + url_values
      data = urllib2.urlopen(full_url)

      #print full_url

      response = data
      the_page = response.read()

      #print the_page
      json_formated = json.loads(the_page)

      pprint(json_formated)

      photos_data = json_formated["photos"]
      if not photos_data:
        print "Nothing here"
      else:
        numberofphotos=len(photos_data)
        photo_data = photos_data[random.randint(0,numberofphotos-1)]
        photo_url = photo_data["photo_file_url"]
        print photo_url
        photo_id = photo_data["photo_id"]
        pic_in_computer = '/home/pi/Desktop/fant-o-matic/pictures/picture-'+str(photo_id)+'.jpg'
        urllib.urlretrieve(photo_url, pic_in_computer)
        display_picture_instruction = "DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority feh --hide-pointer --cycle-once -x -q -D 5 -B black -g 320x240"+" /home/pi/Desktop/fant-o-matic/pictures/picture-"+str(photo_id)+".jpg"
        #print display_picture_instruction
        os.system(display_picture_instruction)
        os.system("sudo python /home/pi/Desktop/fant-o-matic/button.py")
        #sys.exit
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
