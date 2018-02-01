import json
import os
from pyvirtualdisplay import Display
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


# setup of headless xvfb display

display = Display(visible=0, size=(1280, 800))
display.start()





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
    try:
        print "Opening browser"
        f = open("proxies.txt","r")
        proxy_ip = f.read()
        f.close()
        if len(proxy_ip) <=1: #not a valid IP
            print ">>> Not valid IP: No proxy will be used"
            driver = webdriver.Firefox()
        else:
            print "Trying to use proxy: " + proxy_ip
            pport = proxy_ip.split(":")

            PROXY = pport[0]
            PORT = int(pport[1])

            desired_capability = webdriver.DesiredCapabilities.FIREFOX
            desired_capability['proxy']={
                "proxyType":"manual",
                "httpProxy":proxy_ip,
                "ftpProxy":proxy_ip,
                "sslProxy":proxy_ip
            }

            #firefox_profile = webdriver.FirefoxProfile()
            #firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
            #driver = webdriver.Firefox(firefox_profile=firefox_profile,  capabilities=desired_capability)
            driver = webdriver.Firefox()

    except:
        print "REQUEST ERROR: No proxy will be used"
        os.system("python proxy-lister.py")
        driver = webdriver.Firefox()
    return driver





####################
#  CRAWLER
#

# Iterates through US cities database
# src of data: https://gist.github.com/Miserlou/c5cd8364bf9b2420bb29

cities = json.load(open('cities.json'))
count = 0;
for city in cities:
    folder = "{:04d}".format(count)
    if not os.path.exists(folder):
        os.makedirs(folder)

    lat = str(city["latitude"])
    lng = str(city["longitude"])

    print "---"
    print folder + "," + city["city"] + "," + lat + "," + lng

    for frame in range(0, 33):
        driver = open_browser()
        url="https://earthengine.google.com/iframes/timelapse_player_embed.html#v="+lat+","+lng+",10,latLng&t="+"{:.1f}".format(frame/10.)
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

        driver.save_screenshot(folder + "/" + "{:03.0f}".format(frame) + ".png")

        driver.quit()

    count = count + 1


display.stop()
