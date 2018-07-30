from RPi import GPIO
from time import sleep
import time
import threading
import os

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# ==============
# ROTARY ENCODER
# ==============

ROTARYclk = 17
ROTARYdt = 18
ROTARYclick = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(ROTARYclk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ROTARYdt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ROTARYclick, GPIO.IN, pull_up_down=GPIO.PUD_UP)

delayLag = 0
delayLoss = 0
delaySelected = 0
delayChange = 0
clkLastState = GPIO.input(ROTARYclk)

isDirty = 1
firstRun = 1

def handle(pin):
	global clkLastState, counter, delayLag, delayLoss, isDirty
	clkState = GPIO.input(ROTARYclk)
	dtState = GPIO.input(ROTARYdt)
	pressState = GPIO.input(ROTARYclick)

	if clkState != clkLastState:
		if dtState != clkState:
			if delaySelected == 0:
				delayLag += 100
			else:
				delayLoss += 5
		else:
			if delaySelected == 0:
				delayLag -= 100
			else:
				delayLoss -= 5

		delayLag = min(max(delayLag, 0), 5000)
		delayLoss = min(max(delayLoss, 0), 100)
		clkLastState = clkState
		isDirty = 1

GPIO.add_event_detect(ROTARYclk, GPIO.BOTH, handle)
GPIO.add_event_detect(ROTARYdt, GPIO.BOTH, handle)

debounceTime = 0
def clickButton(pin):
	global delaySelected, debounceTime
	if time.time() - debounceTime > 0.2:
		debounceTime = time.time()
		if delaySelected == 0:
			delaySelected = 1
		else:
			delaySelected = 0
		isDirty = 1

GPIO.add_event_detect(ROTARYclick, GPIO.RISING, clickButton)

# ===========
# APPLY DELAY
# ===========

def applyDelay():
	global delayLag, delayLoss, delaySelected, firstRun
	if firstRun == 1:
		command = 'tc qdisc add dev wlan0 root netem delay ' + str(delayLag) + 'ms loss ' + str(delayLoss) + '%'
		firstRun = 0
	else:
		command = 'tc qdisc change dev wlan0 root netem delay ' + str(delayLag) + 'ms loss ' + str(delayLoss) + '%'

	os.system(command)
	print command

# ==============
# DRAW INTERFACE
# ==============

RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=500))

disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
fontA = ImageFont.truetype('/home/pi/LAGBOX/Minecraftia-Regular.ttf', 8)
fontB = ImageFont.truetype('/home/pi/LAGBOX/Minecraftia-Regular.ttf', 14)
#ImageFont.load_default()

def updateUI():
	global image, draw, width, height, fontA, fontB
	global delayLag, delayLoss, delaySelected

	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text((26, 2),  "SSID:  <ENTER SSID>",  font=fontA, fill=255)
	draw.text((38, 12), "PW:  <ENTER PASSWORD>",  font=fontA, fill=255) 

	fillColor = 255
	if delaySelected == 0:
		draw.rectangle((0, 34, 72, 128), outline=255, fill=255)
		fillColor = 0
	draw.text((4, 36), "LAG",  font=fontA, fill=fillColor) 
	draw.text((4, 45), str(delayLag)+"ms",  font=fontB, fill=fillColor) 

	fillColor = 255
	if delaySelected == 1:
		draw.rectangle((75, 34, 128, 128), outline=255, fill=255)
		fillColor = 0
	draw.text((80, 36), "LOSS",  font=fontA, fill=fillColor)
	draw.text((80, 45), str(delayLoss)+"%",  font=fontB, fill=fillColor)

	disp.image(image)
	disp.display()

# =========
# DRAW LOGO
# =========

draw.rectangle((0,0,width,height), outline=0, fill=0)
fontC = ImageFont.truetype('/home/pi/LAGBOX/alagard.ttf', 30)
draw.text((4, 8), "<PROJECT NAME>",  font=fontC, fill=255)
disp.image(image)
disp.display()
sleep(3)

while True:
	if isDirty == 1:
		applyDelay()
		isDirty = 0
		sleep(0.1)
	updateUI()
