import sys
import time
import numpy as np
import socket

sock = socket.socket()
sock.bind(('', 2143))
sock.listen(1)
print('open "opencv.py"')
while True:
	conn, addr = sock.accept()
	conn_f = conn.makefile('rb')
	print("Connection library: ip: " + str(addr[0]))
	data = b' '
	if addr:
		break
def getData():
	data = conn_f.read(2)
	if(data != b''):
		return(ord(data[0]) << 8 | ord(data[1]))
	return None

def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(x, min, max):
        if x > max:
                return max
        elif x < min:
                return min
        else:
                return x
import multiservo
servo = multiservo.Multiservo()
m = [[2, 11, 8, 17], [1, 10, 7, 16], [0, 9, 6, 15]]
import movements
do = movements.quadro(servo)

def default(h = 30):
	set_y(h, 240)
	set_x(90, 240)
	while servo.areMoving():
		pass

def set_x(x, speed):
	servo.write(m[0][0], x, speed)
        servo.write(m[0][1], 180 - x, speed)
        servo.write(m[0][2], x, speed)
        servo.write(m[0][3], 180 - x, speed)
def stop_x():
	servo.stop(m[0][0])
        servo.stop(m[0][1])
        servo.stop(m[0][2])
        servo.stop(m[0][3])
def set_y(y, speed):
	servo.write(m[1][0], y, speed)
        servo.write(m[1][1], y, speed)
        servo.write(m[1][2], y, speed)
        servo.write(m[1][3], y, speed)
        servo.write(m[2][0], y, speed)
        servo.write(m[2][1], y, speed)
        servo.write(m[2][2], y, speed)
        servo.write(m[2][3], y, speed)
def stop_y():
        servo.stop(m[1][0])
        servo.stop(m[1][1])
        servo.stop(m[1][2])
        servo.stop(m[1][3])
        servo.stop(m[2][0])
        servo.stop(m[2][1])
        servo.stop(m[2][2])
        servo.stop(m[2][3])
h = 10
def setHeight(height, width):
	speed_1 = 6
	speed_2 = 2
	global h
	if height <= 230:
		set_y(180, speed_1)
		print("down")
		h = servo.read(m[1][1])
	elif height >= 250:
		set_y(0, speed_1)
		h = servo.read(m[1][1])
		print("up")
	'''
	else:
		for i in range(0, 9):
			do.forward(40, h)
			while(servo.areMoving()):
				pass
		default(h)
	
        if width <= 310:
		set_x(0, speed_2)
        elif width >= 330:
                set_x(180, speed_2)
	else:
		stop_x()
	'''
def dist(dst):

	print(dst)
	if dst >= 75:
		do.back(40, 5)
	elif dst <= 65:
		do.forward(40, 5)
	else:
		default(0)
		do.pos = 0
do.attach_all()
#default()
dst = 0
while True:
	data = getData()
	print(data)
	if data != None:
		dst = data
	else:
		do.detach()
		break
	if dst != 0:
		dist(dst)
