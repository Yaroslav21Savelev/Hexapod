#!/usr/bin/env python3.7
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import PIL
from multiservo import Multiservo
from multiservo import map
from multiservo import constrain
import movements
import ik
#import socketLib
import math
from time import sleep
from time import time
from subprocess import Popen
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
from mpu6050 import mpu6050
from pygame import mixer
#process = Popen(['python', '/home/pi/lcd_cam.py'])
#process = Popen(['python', '/home/pi/host.py'])
#cam_face = Popen(['python', '/home/pi/lcd_cam.py'])
lastTime = time()
g_sensor = mpu6050(0x68)
dsp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
width = dsp.width
height = dsp.height
padding = -2
top = padding
bottom = height-padding
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
font = ImageFont.load_default()
dsp.begin()
dsp.clear()
dsp.display()
servo = Multiservo()
fr = ik.leg(servo, 9, 10, 11, z_offset = 0.5)
fl = ik.leg(servo, 0, 1, 2)
mr = ik.leg(servo, 12, 13, 14, x_offset = -0.5, z_offset = 0)# -0.7556
ml = ik.leg(servo, 3, 4, 5, x_offset = 0, z_offset = 0)
br = ik.leg(servo, 15, 16, 17)
bl = ik.leg(servo, 6, 7, 8)
do = movements.hexa(servo, fr, fl, mr, ml, br, bl)
do.attach_all()
attached = 1
mac = "5C:BA:37:F8:85:11"
mixer.init()
mixer.music.load("/home/pi/startup.mp3")
mixer.music.play()
def update_wlan_oled(con_joy = 0):
	dsp.clear()
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	cmd = str(subprocess.check_output("iwconfig", shell = True).decode())
	ESSID = cmd[cmd.find("ESSID:") + 7:cmd.find('" ', cmd.find("ESSID:") + 6)]
	IP = subprocess.check_output("hostname -I", shell = True)
	draw.text((0, top), "ESSID: " + str(ESSID), font=font, fill=255)
	draw.text((0, top + 8), "IP: " + str(IP.decode()), font=font, fill=255)
	if con_joy:
		temp = "Temp: " + str(g_sensor.get_temp() * 10 // 10)
		draw.text((0, top + 16), "Connecting joy" + temp, font=font, fill=255)
	else:
		temp = "Temp: " + str(g_sensor.get_temp() * 10 // 10)
		draw.text((0, top + 16), temp, font=font, fill=255)
	'''
	if process.poll() is None:
		draw.text((0, top + 24), "Streaming on", font=font, fill=255)
	else:
		draw.text((0, top + 24), "Streaming off", font=font, fill=255)
	'''
	dsp.image(image)
	dsp.display()

try:
	from xbox_controller import joy
	jstk = joy()
	update_wlan_oled(1)
except:
	while True:
		update_wlan_oled(1)
		try:
			cmd = str(subprocess.check_output('echo "connect 5C:BA:37:F8:85:11\nexit" | bluetoothctl', shell = True).decode())
			print(cmd)
			sleep(5)
			from xbox_controller import joy
			jstk = joy()
			update_wlan_oled()
			print("Connected joy")
			break
		except Exception as e:
			print(e)
			print("Try again")






def prop(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
mode = 0
x, y, z = 0, 0, 0
x_, y_, z_ = x, y, z

def quit():
	from sys import exit
	for i in range(18):
		servo.detach(i)
	dsp.clear()
	dsp.display()
	'''
	if process.poll() is None:
		process.terminate()
	'''
	exit()

def menu():
	#global process
	old = 0
	global pos
	try:
		tmp = jstk.read()[11]
	except:
		quit()
	pos = constrain(pos, 1, 3)
	if jstk.read()[0] and pos == 1:
		print("start streaming")
		'''
		if not process.poll() is None:
			#process = Popen(['python', '/home/pi/lcd_cam.py'])
			process = Popen(['python', '/home/pi/host.py'])
		'''
	if jstk.read()[2] and pos == 1:
		print("stop streaming")
		'''
		if process.poll() is None:
				process.terminate()
		'''
	elif jstk.read()[0] and pos == 2:
		mode = 2
	elif jstk.read()[0] and pos == 3:
		quit()
	dsp.clear()
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text((0, top), "Menu", font=font, fill=255)
	if pos == 1:
		draw.text((0, top + 8), ">Stream A-on|Y-off", font=font, fill=255)
		draw.text((0, top + 16), "P2", font=font, fill=255)
		draw.text((0, top + 24), "Quit", font=font, fill=255)
	elif pos == 2:
		draw.text((0, top + 8), "Stream", font=font, fill=255)
		draw.text((0, top + 16), ">P2", font=font, fill=255)
		draw.text((0, top + 24), "Quit", font=font, fill=255)
	elif pos == 3:
		draw.text((0, top + 8), "Stream", font=font, fill=255)
		draw.text((0, top + 16), "P2", font=font, fill=255)
		draw.text((0, top + 24), ">Quit", font=font, fill=255)
	dsp.image(image)
	dsp.display()

def info():
	global lastTime
	if time() - lastTime > 0.5: # update display every 2 seconds
		update_wlan_oled()
		lastTime = time()

def funcs():
	global old
	global mode
	global pos
	pos = constrain(pos, 1, 5)
	if a and pos == 1 and mode != 1: # Walk
		do.go(0, 0, z, 1)
		while(servo.areMoving()):
				pass
		mode = 1

	elif a and pos == 2 and mode != 2: # Agile
		ml.move(5, 0, -5, 30)
		mr.move(5, 0, -5, 30)
		while(servo.areMoving()):
				pass
		mr.move(12, 0, 5, 30)
		ml.move(12, 0, 5, 30)
		while(servo.areMoving()):
				pass
		mode = 2

	elif a and pos == 3 and mode != 3: # Flex
		ml.move(5, 0, -5, 30)
		mr.move(5, 0, -5, 30)
		while(servo.areMoving()):
				pass
		mode = 3

	elif a and pos == 4 and mode != 4: # Tarantul
		x_c, y_c, z_c = 5, 0, -6
		s_speed = 20
		fr.move(3, 2, -9, s_speed)
		fl.move(3, 2, -9, s_speed)
		ml.move(5, 0, -5, s_speed)
		mr.move(5, 0, -5, s_speed)
		br.move(x_c - 0, y_c - 6, z_c + 1.8, s_speed)
		bl.move(x_c - 0, y_c - 6, z_c + 1.8, s_speed)
		while(servo.areMoving()):
				pass
		mr.move(x_c + 1, y_c + 1, z_c - 3.5, s_speed)
		ml.move(x_c + 1, y_c + 1, z_c - 3.5, s_speed)
		while(servo.areMoving()):
				pass
		mode = 4

	elif a and pos == 5 and mode != 5: # Angle
		h = -7
		off = 3
		x = 5
		sp = 40
		ml.move(5, 0, -5, 30)
		mr.move(5, 0, -5, 30)
		while(servo.areMoving()):
				pass
		mr.move(12, 0, 5, 30)
		ml.move(12, 0, 5, 30)
		while(servo.areMoving()):
				pass
		fr.move(x, 0, h, sp)
		fl.move(x, 0, h, sp)
		br.move(x, 0, h, sp)
		bl.move(x, 0, h, sp)
		while(servo.areMoving()):
				pass
		mode = 5

	dsp.clear()
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	if attached:
		draw.text((30, top), "Attached!", font=font, fill=255)
	else:
		draw.text((30, top), "Detached", font=font, fill=255)
	if pos == 1:
		draw.text((0, top + 8), "", font=font, fill=255)
		draw.text((0, top + 16), ">Walk", font=font, fill=255)
		draw.text((0, top + 24), "Agile", font=font, fill=255)
	elif pos == 2:
		draw.text((0, top + 8), "Walk", font=font, fill=255)
		draw.text((0, top + 16), ">Agile", font=font, fill=255)
		draw.text((0, top + 24), "Flexible", font=font, fill=255)
	elif pos == 3:
		draw.text((0, top + 8), "Agile", font=font, fill=255)
		draw.text((0, top + 16), ">Flexible", font=font, fill=255)
		draw.text((0, top + 24), "Tarantul", font=font, fill=255)
	elif pos == 4:
		draw.text((0, top + 8), "Flexible", font=font, fill=255)
		draw.text((0, top + 16), ">Tarantul", font=font, fill=255)
		draw.text((0, top + 24), "Angle", font=font, fill=255)
	elif pos == 5:
		draw.text((0, top + 8), "Tarantul", font=font, fill=255)
		draw.text((0, top + 16), ">Angle", font=font, fill=255)
		draw.text((0, top + 24), "", font=font, fill=255)
	dsp.image(image)
	dsp.display()


class face:
	def __init__(self):
		self.width = dsp.width
		self.height = dsp.height
		padding = -2
		top = padding
		bottom = height-padding
		image = Image.new('1', (width, height))
		draw = ImageDraw.Draw(image)
		draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
		font = ImageFont.load_default()
		self.frame_size = (1280, 720)
		self.frame_center = (self.frame_size[0] // 2, self.frame_size[1] // 2)
		self.camera = PiCamera()
		self.camera.resolution = self.frame_size
		self.camera.framerate = 60
		self.rawCapture = PiRGBArray(self.camera, size=self.frame_size)
		cascPath = "/home/pi/haarcascade_frontalface_default.xml"
		self.faceCascade = cv2.CascadeClassifier(cascPath)
		self.n = 0
		#log.basicConfig(filename='webcam.log',level=log.INFO)
	def detect(self):
		next(self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True))
		frame = self.rawCapture.array
		orig = frame.copy()
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_180)
		faces = self.faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			crop = frame[ y : y + h, x : x + w]
			rszd = cv2.resize(crop, (128, 32), interpolation = cv2.INTER_AREA)
			image = Image.fromarray(rszd).convert("1")
			mixer.music.load("/home/pi/pop.mp3")
			mixer.music.play()
			print("Face_" + str(self.n))
			orig = cv2.rotate(orig, rotateCode=cv2.ROTATE_180)
			cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 255, 0), 2)
			directory = "/home/pi/faces/face_" + str(self.n) + ".jpg"
			cv2.imwrite(directory, orig)
			dsp.image(image)
			dsp.display()
			self.n += 1
		'''
		rszd = cv2.resize(frame, (128, 32), interpolation=cv2.INTER_AREA)
		image = Image.fromarray(rszd).convert("1")
		dsp.image(image)
		dsp.display()
		'''
		self.rawCapture.truncate(0)

face_d = face()
old_dsp = 0 
pos = 1
old = 0
x_old = 0
offset_x = 0
dsp_mode = 0
while True:
	try:
		a = jstk.read()[0]
		x_btn = jstk.read()[3]
		x_cap = jstk.read()[10]
		y_cap = jstk.read()[11]
	except:
		quit()
	if old != y_cap:
		pos = constrain(pos + y_cap, 1, 5)
		old = y_cap
	if old_dsp != x_cap:
		dsp_mode = constrain(dsp_mode + x_cap, 0, 3)
		old_dsp = x_cap
	if jstk.read()[8]:
		servo.holder(0)
	elif jstk.read()[9]:
		servo.holder(1)
	if x_btn and x_old == 0:
		attached = not attached
		if attached:
			do.attach_all()
		else:
			for i in range(18):
				servo.detach(i)
		x_old = 1
	if not x_btn:
		x_old = 0
	if dsp_mode == 0:
		funcs()
	elif dsp_mode == 1:
		menu()
	elif dsp_mode == 2:
		info()
	elif dsp_mode == 3:
		face_d.detect()
	if mode == 1:
		x = jstk.read()[13]
		y = jstk.read()[12]
		if abs(x) >= 1.2 or abs(y) >= 1.2:
			do.go(-y, -x * 1.2, z)
		elif (x_ != x or y_ != y or z_ != z):
			do.go(0, 0, z, 1)
			x_, y_, z_ = x, y, z
	elif mode == 2:
		x = jstk.read()[13]
		y = jstk.read()[12]
		z = jstk.read()[17]
		if(x_ != x or y_ != y or z_ != z):
			do.agile(x, y, z)
			x_, y_, z_ = x, y, z
	elif mode == 3:
		x = jstk.read()[13]
		y = jstk.read()[12]
		z = jstk.read()[17]
		if(x_ != x or y_ != y or z_ != z):
			do.flex(x, y, z)
			x_, y_, z_ = x, y, z

	elif mode == 4: # Tarantul
		sp = 200
		x_l = map(jstk.read()[14], -2.5, 2.5, 60, 0)
		y_l = map(jstk.read()[15], 2.5, -2.5, 110, 0)
		x_r = map(jstk.read()[13], 2.5, -2.5, 60, 0)
		y_r = map(jstk.read()[12], 2.5, -2.5, 110, 0)
		z_l = map(jstk.read()[16], -3.0, 3.0, 130, 40)
		z_r = map(jstk.read()[17], -3.0, 3.0, 130, 40)
		servo.write(0, x_l, sp)
		servo.write(9, x_r, sp)
		servo.write(1, y_l, sp)
		servo.write(10, y_r, sp)
		servo.write(2, z_l, sp)
		servo.write(11, z_r, sp)
		#fr.move(4 + x_r * 0.8, 8.5 - z_r * 0.8, -3.5 - y_r, 100)
		#fl.move(4 - x_l * 0.8, 8.5 - z_l * 0.8, -3.5 - y_l, 100)

	elif mode == 5:
		from math import pi, sin, radians, asin
		sp = 15
		h = -7
		off = 3
		x = 5
		ang_y, ang_x = g_sensor.get_accel_data()["x"], g_sensor.get_accel_data()["y"]
		if ang_y >= 0.5:
			if ang_x >= -1.5:
				fl.move(x, 0, h + off, sp)
				br.move(x, 0, h - off, sp)
			elif ang_x <= -2.5:
				fr.move(x, 0, h + off, sp)
				bl.move(x, 0, h - off, sp)
			else:
				fr.move(x, 0, h + off, sp)
				fl.move(x, 0, h + off, sp)
				br.move(x, 0, h - off, sp)
				bl.move(x, 0, h - off, sp)
		
		elif ang_y <= -0.5:
			if ang_x >= -1.5:
				fl.move(x, 0, h - off, sp)
				br.move(x, 0, h + off, sp)
			elif ang_x <= -2.5:
				fr.move(x, 0, h - off, sp)
				bl.move(x, 0, h + off, sp)
			else:
				fr.move(x, 0, h - off, sp)
				fl.move(x, 0, h - off, sp)
				br.move(x, 0, h + off, sp)
				bl.move(x, 0, h + off, sp)
		elif ang_x >= -1.5:
			fr.move(x, 0, h - off, sp)
			fl.move(x, 0, h + off, sp)
			br.move(x, 0, h - off, sp)
			bl.move(x, 0, h + off, sp)
		elif ang_x <= -2.5:
			fr.move(x, 0, h + off, sp)
			fl.move(x, 0, h - off, sp)
			br.move(x, 0, h + off, sp)
			bl.move(x, 0, h - off, sp)
		else:
			for i in range(18):
				servo.stop(i)
		sleep(0.08)
