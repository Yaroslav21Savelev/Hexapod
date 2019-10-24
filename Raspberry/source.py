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
	tmp = 9999
	x, y, z, mode = 0, 0, 0, 9999
	pos = 1
	while True:
		try:
			x, y, z, tmp = jstk.update(x, y, z, mode)
		except:
			quit()
		if mode != tmp:
			if tmp == 25:
				return
			elif tmp == 36:
				pos = constrain(pos + 1, 1, 3)
			elif tmp == 35:
				pos = constrain(pos - 1, 1, 3)
			elif tmp == 3 and pos == 3:
				quit()
			elif tmp == 3 and pos == 1:
				#print(process.poll())
				if not process.poll() is None:
					process = Popen(['python', '/home/pi/host.py'])
			elif tmp == 10 and pos == 1:
				#print(process.poll())
				if process.poll() is None:
					process.terminate()
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

while True:
	try: # try to get new data from joy, except terminate process
		x, y, z, tmp = jstk.update(x, y, z, mode)
	except:
		quit()
	if time() - lastTime > 2: # update display every 2 seconds
		update_wlan_oled()
		lastTime = time()
	if mode != tmp:
		if tmp == 10: #attach/detach
			attached = not attached
			if attached:
				do.attach_all()
			else:
				for i in range(18):
					servo.detach(i)
		elif tmp == 30:
			servo.holder(0)
		elif tmp == 31:
			servo.holder(1)
		elif tmp == 4:
			mode = tmp
			x_c, y_c, z_c = 5, 0, -6
			s_speed = 40
			fr.move(3, 7, -3, s_speed)
			fl.move(3, 7, -3, s_speed)
			mr.move(x_c + 1, y_c + 1, z_c - 3.5, s_speed)
			ml.move(x_c + 2, y_c + 1, z_c - 3.5, s_speed)
			br.move(x_c - 0, y_c - 6, z_c + 1.8, s_speed)
			bl.move(x_c - 0, y_c - 6, z_c + 1.8, s_speed)
		elif tmp == 25:
			tmp = 0
			menu()
		else:
			mode = tmp
		#pos = 0
	if mode == 1:
		#print(x, y)
		if abs(x) >= 0.5 or abs(y) >= 0.5:
			do.go(-y, -x * 1.2, z)
		elif (x_ != x or y_ != y or z_ != z):
			do.go(0, 0, z, 1)
			x_, y_, z_ = x, y, z
	elif mode == 2:
		if(x_ != x or y_ != y or z_ != z):
			do.agile(x, y, z)
			x_, y_, z_ = x, y, z
	elif mode == 3:
		if(x_ != x or y_ != y or z_ != z):
			do.flex(x, y, z)
			x_, y_, z_ = x, y, z
	elif mode == 4:
		if(x_ != x or y_ != y or z_ != z):
			fr.move(4 + x * 0.8, 8.5 - z * 0.8, -5 - y, 250)
			fl.move(3, 7, -3, 250)
			x_, y_, z_ = x, y, z
	


