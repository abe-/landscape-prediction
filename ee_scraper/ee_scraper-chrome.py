import json
import os
import sys
import subprocess
#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *
from time import sleep




####################
#  INITIAL SETUP
#


zoom = str(9)

# setup of headless xvfb display

#display = Display(visible=0, size=(1154, 669)) # to obtain 1024x512 screengrabs
#display.start()





####################
#  TOOLS
#

# Detects when Earth Engine Timelapse has loaded the canvas with image

class canvas_check():
  def __init__(self):
      self = self
  def __call__(self,driver):
    driver.execute_script("var canvas2 = document.getElementById('blank'); if (canvas2 != null) document.body.removeChild(canvas2);")
    driver.execute_script("var canvas2=document.getElementById('timeMachine_timelapse_canvas').cloneNode();canvas2.id='blank';canvas2.display='none';document.body.appendChild(canvas2);")
    return driver.execute_script("if (document.getElementById('timeMachine_timelapse_canvas').toDataURL() != document.getElementById('blank').toDataURL() && document.getElementsByClassName('spinnerOverlay')[0].offsetParent == null) return true; else return false;")


# Creates a browser instance that goes through a proxy

def open_browser():
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    options.add_argument('window-size=512, 512')
    options.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=options)
    return driver





####################
#  CRAWLER
#

# Iterates through json with geo points

filename = sys.argv[1]
points = json.load(open(filename+'.json'))

outputdir = "../Data/Train-" + filename + "/"
if not os.path.exists(outputdir): os.makedirs(outputdir)

count = 0
for count in range(len(points)):
  if count > -1:
    point = points[count]
    folder = point["id"]

    tfold = os.path.join(outputdir, folder)
    if not os.path.exists(tfold): os.makedirs(tfold)

    lat = str(point["latitude"])
    lng = str(point["longitude"])

    print "---"
    print folder + "," + lat + "," + lng

    driver = open_browser()

    for frame in range(0, 33):

        url="https://earthengine.google.com/iframes/timelapse_player_embed.html#v="+lat+","+lng+","+zoom+",latLng&t="+"{:.1f}".format(frame/10.)
        driver.get(url)

        try:
            wait = WebDriverWait(driver, 10, poll_frequency=3)
            #element = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'spinnerOverlay')))
            element = wait.until(canvas_check())
            #myElem = WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'spinnerOverlay')))
            print "Page is ready!"
        except TimeoutException:
            print "Loading took too much time!"

        driver.execute_script("var i1=document.getElementById('scaleBar1_scaleBarContainer');if(i1) i1.style.display = 'none';")
        driver.execute_script("var i2=document.getElementById('contextMap1_contextMapContainer');if(i2) i2.style.display = 'none';")
        driver.execute_script("var i3=document.getElementsByClassName('sideToolBar')[0];if(i3) i3.style.display='none';")
        driver.execute_script("var i4=document.getElementsByClassName('customControl')[0];if(i4) i4.style.display='none';")

        fn = os.path.join(outputdir, folder, "{:03.0f}".format(frame) + ".png")
        driver.save_screenshot(fn)

    driver.quit()

    numtiles = 0
    for frame in range(0,33):
	tmp = outputdir+"{:03.0f}".format(frame)+".png"
        for tile in range(numtiles):
                tiledir = outputdir+folder+"-"+str(tile)+"/"
                if not os.path.exists(tiledir):
                        os.makedirs(tiledir)

        print "Croping frame " + str(frame)

        if numtiles == 32:
            cmd ="/opt/ImageMagick/bin/convert "+ os.path.join(tmp)+ " -crop 4x2@ +repage +adjoin "+ outputdir+folder+"-%d/"+"{:03.0f}".format(frame) + ".png"
            subprocess.call(cmd,shell=True)
        elif numtiles == 2:
            cmd ="/opt/ImageMagick/bin/convert "+ os.path.join(tmp)+ " -crop 2x1@ +repage +adjoin "+ outputdir+folder+"-%d/"+"{:03.0f}".format(frame) + ".png"
            subprocess.call(cmd,shell=True)
#display.stop()
