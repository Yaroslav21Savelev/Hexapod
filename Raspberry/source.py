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
#from mpu6050 import mpu6050
process = Popen(['python', '/home/pi/host.py'])
lastTime = time()
#g_sensor = mpu6050(0x68)
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
fr = ik.leg(servo, 9, 10, 11)
fl = ik.leg(servo, 0, 1, 2)
mr = ik.leg(servo, 12, 13, 14, x_offset = 0)# -0.7556
ml = ik.leg(servo, 3, 4, 5, x_offset = 0)
br = ik.leg(servo, 15, 16, 17)
bl = ik.leg(servo, 6, 7, 8)
do = movements.hexa(servo, fr, fl, mr, ml, br, bl)
do.attach_all()
attached = 1
mac = "5C:BA:37:F8:85:11"

def update_wlan_oled(con_joy = 0):
	dsp.clear()
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	cmd = str(subprocess.check_output("iwconfig", shell = True).decode())
	ESSID = cmd[cmd.find("ESSID:") + 7:cmd.find('" ', cmd.find("ESSID:") + 6)]
	#print(ESSID)
	IP = subprocess.check_output("hostname -I", shell = True)
	draw.text((0, top), "ESSID: " + str(ESSID), font=font, fill=255)
	draw.text((0, top + 8), "IP: " + str(IP.decode()), font=font, fill=255)
	if con_joy:
		draw.text((0, top + 16), "Connecting joy", font=font, fill=255)
	else:
		from time import localtime
		sec = localtime().tm_sec
		if attached:
			draw.text((0, top + 16), "Attached " + str(sec), font=font, fill=255)
		else:
			draw.text((0, top + 16), "Detached " + str(sec), font=font, fill=255)
	if process.poll() is None:
		draw.text((0, top + 24), "Streaming on", font=font, fill=255)
	else:
		draw.text((0, top + 24), "Streaming off", font=font, fill=255)
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
	if process.poll() is None:
		process.terminate()
	exit()

def menu():
	global process
	old = 0
	pos = 1
	while jstk.read()[4]:
		pass
	while True:
		try:
			tmp = jstk.read()[11]
		except:
			quit()
		if jstk.read()[4]:
			return
		if old != tmp:
			pos = constrain(pos + tmp, 1, 3)
			old = tmp
		if jstk.read()[0] and pos == 1:
			print("start streaming")
			if not process.poll() is None:
				process = Popen(['python', '/home/pi/host.py'])
		if jstk.read()[3] and pos == 1:
			print("stop streaming")
			if process.poll() is None:
					process.terminate()
		elif jstk.read()[0] and pos == 2:
			mode = 2
		elif jstk.read()[0] and pos == 3:
			quit()
		dsp.clear()
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		draw.text((0, top), "Menu", font=font, fill=255)
		if pos == 1:
			draw.text((0, top + 8), ">Stream A-on|X-off", font=font, fill=255)
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
	while jstk.read()[5]:
		pass
	while True:
		if jstk.read()[5]:
				return
		if time() - lastTime > 0.5: # update display every 2 seconds
			update_wlan_oled()
			lastTime = time()
		

pos = 1
old = 0
x_old = 0
while True:
	try:
		tmp = jstk.read()[11]
		a = jstk.read()[0]
	except:
		quit()
	if jstk.read()[8]:
		servo.holder(0)
	elif jstk.read()[9]:
		servo.holder(1)
			
	if jstk.read()[4]:
		menu()
	while jstk.read()[4]:
		pass
	if jstk.read()[5]:
		info()
	while jstk.read()[5]:
		pass
	x = jstk.read()[3]
	if x and x_old == 0:
		attached = not attached
		if attached:
			do.attach_all()
		else:
			for i in range(18):
				servo.detach(i)
		x_old = 1
	if not x:
		x_old = 0
	if old != tmp:
		print(pos, tmp, a)
		pos = constrain(pos + tmp, 1, 4)
		old = tmp
	if a and pos == 1 and mode != 1:
		mode = 1
	elif a and pos == 2 and mode != 2:
		mode = 2
	elif a and pos == 3 and mode != 3:
		mode = 3
	elif a and pos == 4 and mode != 4:
		x_c, y_c, z_c = 5, 0, -6
		s_speed = 40
		fr.move(3, 7, -3, s_speed)
		fl.move(3, 7, -3, s_speed)
		mr.move(x_c + 1, y_c + 1, z_c - 3.5, s_speed)
		ml.move(x_c + 2, y_c + 1, z_c - 3.5, s_speed)
		br.move(x_c - 0, y_c - 6, z_c + 1.8, s_speed)
		bl.move(x_c - 0, y_c - 6, z_c + 1.8, s_speed)
		mode = 4
	dsp.clear()
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	if attached:
		draw.text((0, top), "Attached!", font=font, fill=255)
	else:
		draw.text((0, top), "Detached", font=font, fill=255)
	if pos == 1:
		draw.text((0, top + 8), "", font=font, fill=255)
		draw.text((0, top + 16), ">Walk", font=font, fill=255)
		draw.text((0, top + 24), "Agile", font=font, fill=255)
	elif pos == 2:
		draw.text((0, top + 8), "Walk", font=font, fill=255)
		draw.text((0, top + 16), ">Agile", font=font, fill=255)
		draw.text((0, top + 24), "Flex", font=font, fill=255)
	elif pos == 3:
		draw.text((0, top + 8), "Agile", font=font, fill=255)
		draw.text((0, top + 16), ">Flex", font=font, fill=255)
		draw.text((0, top + 24), "Tarantul", font=font, fill=255)
	elif pos == 4:
		draw.text((0, top + 8), "Flex", font=font, fill=255)
		draw.text((0, top + 16), ">Tarantul", font=font, fill=255)
		draw.text((0, top + 24), "", font=font, fill=255)
	dsp.image(image)
	dsp.display()
	if mode == 1:
		x = jstk.read()[13]
		y = jstk.read()[12]
		if abs(x) >= 0.5 or abs(y) >= 0.5:
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
	elif mode == 4:
		x_l = jstk.read()[14]
		y_l = jstk.read()[15]
		x_r = jstk.read()[13]
		y_r = jstk.read()[12]
		z_l = jstk.read()[16]
		z_r = jstk.read()[17]
		fr.move(4 + x_r * 0.8, 8.5 - z_r * 0.8, -5 - y_r, 250)
		fl.move(4 + x_l * 0.8, 8.5 - z_l * 0.8, -5 - y_l, 250)
	


