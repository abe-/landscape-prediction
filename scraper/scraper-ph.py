import json
import os
import sys, argparse
import subprocess
#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *
from time import sleep
from settings import *
from PIL import Image


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
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
    )
    driver = webdriver.PhantomJS(executable_path="/Users/agfm1n14/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs",desired_capabilities=dcap)
    driver.set_window_size(512,512)
    return driver





####################
#  CRAWLER
#

# Iterates through json with geo points

parser = argparse.ArgumentParser()
parser.add_argument('--json', metavar='json',
                    help='json file with points information')

args = parser.parse_args()
if args.json and os.path.exists(args.json):
    points = json.load(open(args.json))
else:
    points = json.load(open(KEY+".json"))

outputdir = os.path.join(TRAIN_DIR)
if not os.path.exists(outputdir): os.makedirs(outputdir)

count = 0
for count in range(len(points)):
  if count > -1:
    point = points[count]
    folder = KEY + "-" + str(point["id"])

    tfold = os.path.join(outputdir, folder)
    if not os.path.exists(tfold): os.makedirs(tfold)

    lat = str(point["latitude"])
    lng = str(point["longitude"])

    print "---"
    print folder + "," + lat + "," + lng

    driver = open_browser()

    for frame in range(0, 33):

        url="https://earthengine.google.com/iframes/timelapse_player_embed.html#v="+lat+","+lng+","+str(ZOOM)+",latLng&t="+"{:.1f}".format(frame/10.)
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

    
    _, _, files = os.walk( tfold ).next()
    
    ct = 0
    for f in files:
        print "Croping frame " + str(ct)
        maxdim = max(WIDTH,HEIGHT)
        box = (0, 0, maxdim, maxdim)

        path_downloaded = os.path.join( tfold, f )
        im = Image.open(path_downloaded)
        region = im.crop(box)
        fname = os.path.splitext(f)[0]
        path_frame = os.path.join(tfold, fname+".jpg");

        region.save(path_frame, 'JPEG', optimize=True, quality=95)
        os.remove(path_downloaded)

        ct = ct + 1