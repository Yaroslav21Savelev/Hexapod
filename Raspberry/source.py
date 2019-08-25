from multiservo import Multiservo
from multiservo import map
import movements
import ik
import socketLib
import math
from time import sleep
servo = Multiservo()
do = movements.quadro(servo)
do.attach_all()

fr = ik.leg(servo, 11, 10, 9)
br = ik.leg(servo, 15, 16, 17)
bl = ik.leg(servo, 6, 7, 8)
fl = ik.leg(servo, 2, 1, 0)






pos = 0
def forward():
	x, y, z = 6, 2, -6
	x_b, y_b, z_b = 7, 0, -9
	h = 2
	l = 3
	low = 50
	fast = 150
	s_d = 70
	h_ = 2
	global pos
	if(servo.areMoving()):
			return
	elif pos == 0:
		fr.move(x, y - l, z + h, fast)
	elif pos == 1:
		fr.move(x, y + l, z + h, fast)
	elif pos == 2:
		fr.move(x, y + l, z + h_, s_d)
	elif pos == 3:
		bl.move(x_b, y_b - 1, z_b + h, fast)
	elif pos == 4:
		bl.move(x_b, y_b + l, z_b + h, fast)
	elif pos == 5:
		bl.move(x_b, y_b + l, z_b, s_d)
	elif pos == 6:
		fr.move(x, y, z, low)
		bl.move(x_b, y_b, z_b, low)
		fl.move(x, y - l, z, low)
		br.move(x_b, y_b - l, z_b, low)
	elif pos == 7:
		fl.move(x, y - l, z + h, fast)
	elif pos == 8:
		fl.move(x, y + l, z + h, fast)
	elif pos == 9:
		fl.move(x, y + l, z + h_, s_d)
	elif pos == 10:
		br.move(x_b, y_b - l, z_b + h, fast)
	elif pos == 11:
		br.move(x_b, y_b + l, z_b + h, fast)
	elif pos == 12:
		br.move(x_b, y_b + l, z_b, s_d)
	elif pos == 13:
		fr.move(x, y - l, z, low)
		bl.move(x_b, y_b - l, z_b, low)
		fl.move(x, y, z, low)
		br.move(x_b, y_b, z_b, low)
	else:
		pos = 0
		return
	pos += 1



def back():
	x, y, z = 7, 0, -8
	x_b, y_b, z_b = 6, -3, -6
	h = 2
	l = -3
	low = 50
	fast = 150
	s_d = 70
	h_ = 0.5
	global pos
	if(servo.areMoving()):
			return
	elif pos == 0:
		bl.move(x_b, y_b - 1, z_b + h, fast)
	elif pos == 1:
		bl.move(x_b, y_b + l, z_b + h, fast)
	elif pos == 2:
		bl.move(x_b, y_b + l, z_b + h_, s_d)
	elif pos == 3:
		fr.move(x, y - l, z + h, fast)
	elif pos == 4:
		fr.move(x, y + l, z + h, fast)
	elif pos == 5:
		fr.move(x, y + l, z, s_d)
	elif pos == 6:
		fr.move(x, y, z, low)
		bl.move(x_b, y_b, z_b, low)
		fl.move(x, y - l, z, low)
		br.move(x_b, y_b - l, z_b, low)
	elif pos == 7:
		br.move(x_b, y_b - l, z_b + h, fast)
	elif pos == 8:
		br.move(x_b, y_b + l, z_b + h, fast)
	elif pos == 9:
		br.move(x_b, y_b + l, z_b + h_, s_d)
	elif pos == 10:
		fl.move(x, y - l, z + h, fast)
	elif pos == 11:
		fl.move(x, y + l, z + h, fast)
	elif pos == 12:
		fl.move(x, y + l, z, s_d)
	elif pos == 13:
		fr.move(x, y - l, z, low)
		bl.move(x_b, y_b - l, z_b, low)
		fl.move(x, y, z, low)
		br.move(x_b, y_b, z_b, low)
	else:
		pos = 0
		return
	pos += 1


'''
		bl.move(x_b, y_b, z_b, fast)
		fl.move(x, y, z, fast)
		br.move(x_b, y_b, z_b, fast)
'''

def left():
	x, y, z = 5, 0, -10
	x_b, y_b, z_b = 5, 0, -10
	h = 2
	l = 4
	low = 50
	fast = 180
	s_d = 60
	global pos
	if(servo.areMoving()):
		return
	elif pos == 0:
		fr.move(x + l, y, z + h, fast)
	elif pos == 1:
		fr.move(x - l, y, z + h, fast)
	elif pos == 2:
		fr.move(x - l, y, z, s_d)
	elif pos == 3:
		bl.move(x_b - l, y_b, z_b + h, fast)
	elif pos == 4:
		bl.move(x_b + l, y_b, z_b + h, fast)
	elif pos == 5:
		bl.move(x_b + l, y_b, z_b, s_d)
	elif pos == 6:
		fr.move(x, y, z, low)
		bl.move(x_b, y_b, z_b, low)
		fl.move(x, y - l, z, low)
		br.move(x_b, y_b + l, z_b, low)
	elif pos == 7:
		fl.move(x - l, y, z + h, fast)
	elif pos == 8:
		fl.move(x + l, y, z + h, fast)
	elif pos == 9:
		fl.move(x + l, y, z, s_d)
	elif pos == 10:
		br.move(x_b + l, y_b, z_b + h, fast)
	elif pos == 11:
		br.move(x_b - l, y_b, z_b + h, fast)
	elif pos == 12:
		br.move(x_b - l, y_b, z_b, s_d)
	elif pos == 13:
		fr.move(x + l, y, z, low)
		bl.move(x_b - l, y_b, z_b, low)
		fl.move(x, y, z, low)
		br.move(x_b, y_b, z_b, low)
	else:
		pos = 0
		return
	pos += 1


try:
	addr = sys.argv[1]
except:
	 addr = "192.168.0.123"
print("on")
session = socketLib.client(addr, 4219)
print("on")
session.connect()
print("on")





def prop(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
mode = 0
x, y, z = 0, 0, 0
x_, y_, z_ = x, y, z
while True:
	data = session.read()
	if not data is None:
		if data == "forward":
			mode = 1
		elif data == "back":
			mode = -1
		elif data == "stop":
			mode = 0
			fr.move(5, 0, -8)
			bl.move(5, 0, -8)
			fl.move(5, 0, -8)
			br.move(5, 0, -8)
		elif data == "agile":
			mode = 2
		elif data == "attach":
			do.attach_all()
		elif data == "detach":
			mode = 10
			for i in range(18):
				servo.detach(i)
		else:
			#print(data)
			if data[0] == "2":
				z = int(data[2:len(data)])
				z = map(z, -100, 100, -3.0, 3.0)
				z = round(z, 1)
				print("z", z)
			if data[0] == "3":
				y = int(data[2:len(data)])
				y = map(y, -100, 100, -4.0, 4.0)
				y = round(y, 1)
				print("y", y)
			if data[0] == "4":
				x = int(data[2:len(data)])
				x = map(x, -100, 100, -3.0, 3.0)
				x = round(x, 1)
				print("x", x)
			
			
			
	if mode == 2:
		if(x_ != x or y_ != y or z_ != z):
			fr.move(7 - x, y, -7 + z, 80)
			bl.move(7 + x, y, -7 + z, 80)
			fl.move(7 + x, y, -7 + z, 80)
			br.move(7 - x, y, -7 + z, 80)
			x_, y_, z_ = x, y, z
	elif mode == 1:
		forward()
	elif mode == -1:
		back()


