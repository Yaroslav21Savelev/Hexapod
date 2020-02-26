class hexa():
	def __init__(self, servo, fr, fl, mr, ml, br, bl):
		self.fr = fr
		self.fl = fl
		self.mr = mr
		self.ml = ml
		self.br = br
		self.bl = bl
		self.pos = 0
		self.servo = servo
		self.l = 1
		self.f = 1
		self.k = 0
		
	def attach_all(self):
		servo = self.servo
		import json
		with open("/home/pi/pulseWidth.json", "r") as read_file:
			srv = json.load(read_file)
			for i in srv["left"].items():
				for s in i[1]:
					servo.attach(s[0], s[1], s[2])
			for i in srv["right"].items():
				for s in i[1]:
					servo.attach(s[0], s[1], s[2])

	def map(self, x, in_min, in_max, out_min, out_max):
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
	def detach(self):
		servo = self.servo
		for i in range(18):
			servo.detach(i)
	def constrain(self, x, min, max):
		if x > max:
			return max
		elif x < min:
			return min
		else:
			return x
	def go(self, y_, x_, z_, start = 0):
		fr = self.fr
		fl = self.fl
		mr = self.mr
		ml = self.ml
		br = self.br
		bl = self.bl
		pos = self.pos
		l = self.l
		f = self.f
		x, y, z = 5, 0, -6
		#fz, bz = -self.constrain(self.k, 0, 2), self.constrain(self.k, 0, 2)
		fz, bz = 0, 0
		h = 1.5
		low = 35
		fast = 130
		s_speed = 30
		if(self.servo.areMoving()):
				return
		elif start:
			self.l = y_
			self.f = x_
			self.k = z_
			l = y_
			f = x_
			fr.move(x + f, y - l, z + fz, s_speed)
			ml.move(x - f, y - l, z, s_speed)
			br.move(x + f, y - l, z + bz, s_speed)
			fl.move(x, y, z + fz, s_speed)
			mr.move(x, y, z, s_speed)
			bl.move(x, y, z + bz, s_speed)
			self.pos = 0
		elif pos == 0:
			self.l = y_
			self.f = x_
			self.k = z_
			l = y_
			f = x_
			fr.move(x + f, y - l, z + fz + h, fast)
			ml.move(x - f, y - l, z + h, fast)
			br.move(x + f, y - l, z + bz + h, fast)
		elif pos == 1:
			fr.move(x - f, y + l, z + fz + h, fast)
			ml.move(x + f, y + l, z + h, fast)
			br.move(x - f, y + l, z + bz + h, fast)
		elif pos == 2:
			fr.move(x - f, y + l, z + fz, low)
			ml.move(x + f, y + l, z, low)
			br.move(x - f, y + l, z + bz, low)
		elif pos == 3:
			fr.move(x, y, z + fz, low)
			ml.move(x, y, z, low)
			br.move(x, y, z + bz, low)

			fl.move(x - f, y - l, z + fz, low)
			mr.move(x + f, y - l, z, low)
			bl.move(x - f, y - l, z + bz, low)
		elif pos == 4:
			fl.move(x - f, y - l, z + fz + h, fast)
			mr.move(x + f, y - l, z + h, fast)
			bl.move(x - f, y - l, z + bz + h, fast)
		elif pos == 5:
			fl.move(x + f, y + l, z + fz + h, fast)
			mr.move(x - f, y + l, z + h, fast)
			bl.move(x + f, y + l, z + bz + h, fast)
		elif pos == 6:
			fl.move(x + f, y + l, z + fz, low)
			mr.move(x - f, y + l, z, low)
			bl.move(x + f, y + l, z + bz, low)
		elif pos == 7:
			fl.move(x, y, z + fz, low)
			mr.move(x, y, z, low)
			bl.move(x, y, z + bz, low)

			fr.move(x + f, y - l, z + fz, low)
			ml.move(x - f, y - l, z, low)
			br.move(x + f, y - l, z + bz, low)
		else:
			self.pos = 0
			return
		self.pos += 1
	def rotate(self):
		fr = self.fr
		fl = self.fl
		mr = self.mr
		ml = self.ml
		br = self.br
		bl = self.bl
		pos = self.pos
		x, y, z = 4.5, 0, -6
		l = 3
		h = 0
		low = 30
		fast = 130
		x_, y_, z_ = 1, 3, 0
		if(self.servo.areMoving()):
				return
		elif pos == 0:
			fl.move(x, y, z, low)
			mr.move(x, y, z, low)
			bl.move(x, y, z, low)

			fr.move(x, y, z, low)
			ml.move(x, y, z, low)
			br.move(x, y, z, low)
		elif pos == 1:
			'''
			fl.move(x + l, y - l, z, low)
			#mr.move(x, y, z, low)
			bl.move(x + l, y - l, z, low)

			fr.move(x + l, y + l, z, low)
			#ml.move(x, y, z, low)
			br.move(x + l, y + l, z, low)
			'''
			fl.move(x, y - l, z, low)
			ml.move(x, y - l, z, low)
			bl.move(x, y - l, z, low)

			fr.move(x, y + l, z, low)
			mr.move(x, y + l, z, low)
			br.move(x, y + l, z, low)
		else:
			self.pos = 0
			return
		self.pos += 1
	def square(self):
		fr = self.fr
		fl = self.fl
		mr = self.mr
		ml = self.ml
		br = self.br
		bl = self.bl
		pos = self.pos
		low  = 120
		h = -5.2
		from time import sleep
		from numpy import arange
		'''
		import numpy as np
		from math import pi
		import math
		def PointsInCircum(r, n=100):
			return [(math.cos(2 * pi / n * x) * r, math.sin(2 * pi / n * x) * r) for x in range(0, n+1)]
		#print(PointsInCircum(4))
		fl.move(3 , 6, h, low)
		sleep(1)
		fl.move(3 , 6, h + 1, low)
		sleep(1)
		for a in PointsInCircum(2, n = 300):
			i = list(map(float, a,))
			print(i)
			i[0] = i[0]
			i[1] = i[1]
			print(i[1] + 3, i[0])
			fl.move(i[1]  + 3 , i[0] + 7, h, low)
			sleep(0.01)
		print("----")
		fl.move(3 , 4, h + 1, low)
		sleep(1)
		'''
		if(self.servo.areMoving()):
				return
		elif pos == 0:
			for i in arange(0, 4, 0.02):
				fl.move(10 - i, 1, h, low)
				sleep(0.01)
		elif pos == 1:
			for i in arange(0, 4, 0.02):
				fl.move(6, 1 + i, h, low)
				sleep(0.01)
		elif pos == 2:
			for i in arange(0, 4, 0.02):
				fl.move(6 + i, 5, h, low)
				sleep(0.01)
		elif pos == 3:
			for i in arange(0, 4, 0.02):
				fl.move(10, 5 - i, h, low)
				sleep(0.01)
		else:
			self.pos = 0
			return
		self.pos += 1
		
	def agile(self, x, y, z):
		fr = self.fr
		fl = self.fl
		mr = self.mr
		ml = self.ml
		br = self.br
		bl = self.bl
		x_ = 5
		x = self.map(x, -2.5, 2.5, -2.0, 2.0)
		z = self.map(z, -3.0, 3.0, -10.0, -6)
		fr.move(x_ - x, 1.5 + y, z, 60)
		fl.move(x_ + x, 1.5 + y, z, 60)
		
		br.move(x_ - x + 1, -1.5 + y, z + 1, 60)
		bl.move(x_ + x + 1, -1.5 + y, z + 1, 60)

	def flex(self, x, y, z):
		fr = self.fr
		fl = self.fl
		mr = self.mr
		ml = self.ml
		br = self.br
		bl = self.bl
		x_ = 6
		start = -6.5
		x = x / 1.5
		y = self.constrain(y / 1.2, -2, 1)
		fr.move(x_, 2 , start - y + x, 60)
		fl.move(x_, 2 , start - y - x, 60)
		mr.move(x_ + 1, 0 , start + x, 60)
		ml.move(x_ + 1, 0 , start - x, 60)
		br.move(x_, -2 , start + y + x, 60)
		bl.move(x_, -2 , start + y - x, 60)
	def dance(self):
		fr = self.fr
		fl = self.fl
		mr = self.mr
		ml = self.ml
		br = self.br
		bl = self.bl
		from time import time
		t = time()
		while time() - t <= 9:
			self.go(0.3, 0, 0)
		do.go(0, 0, 0, 1)
		while self.servo.areMoving():
			pass
		sp = 9
		sp_f = 60
		z = -6.5
		t = time()
		p = 0
		while time() - t <= 29:
			if p == 0:
				fr.move(8, 0, z, sp)
				fl.move(2, 0, z, sp)
				br.move(8, 0, z, sp)
				bl.move(2, 0, z, sp)
				while self.servo.areMoving():
					pass
				fr.move(5, 0, z, sp_f)
				fl.move(5, 0, z, sp_f)
				br.move(5, 0, z, sp_f)
				bl.move(5, 0, z, sp_f)
				while self.servo.areMoving():
					pass
				p += 1
			elif p == 1:
				fr.move(2, 0, z, sp)
				fl.move(8, 0, z, sp)
				br.move(2, 0, z, sp)
				bl.move(8, 0, z, sp)
				while self.servo.areMoving():
					pass
				fr.move(5, 0, z, sp_f)
				fl.move(5, 0, z, sp_f)
				br.move(5, 0, z, sp_f)
				bl.move(5, 0, z, sp_f)
				while self.servo.areMoving():
					pass
				p += 1
			else:
				p = 0
		sp = 30
		sp_f = 40
		t = time()
		p = 0
		while time() - t <= 13:
			if p == 0:
				fr.move(6, 2, z, sp)
				fl.move(4, 2, z, sp)
				br.move(6, 2, z, sp)
				bl.move(4, 2, z, sp)
				while self.servo.areMoving():
					pass
				fr.move(6, -2, z, sp)
				fl.move(4, -2, z, sp)
				br.move(6, -2, z, sp)
				bl.move(4, -2, z, sp)
				while self.servo.areMoving():
					pass
				fr.move(5, 0, z, sp_f)
				fl.move(5, 0, z, sp_f)
				br.move(5, 0, z, sp_f)
				bl.move(5, 0, z, sp_f)
				while self.servo.areMoving():
					pass
				p += 1
			if p == 1:
				fr.move(4, -2, z, sp)
				fl.move(6, -2, z, sp)
				br.move(4, -2, z, sp)
				bl.move(6, -2, z, sp)
				
				while self.servo.areMoving():
					pass
				fr.move(4, 2, z, sp)
				fl.move(6, 2, z, sp)
				br.move(4, 2, z, sp)
				bl.move(6, 2, z, sp)
				while self.servo.areMoving():
					pass
				fr.move(5, 0, z, sp_f)
				fl.move(5, 0, z, sp_f)
				br.move(5, 0, z, sp_f)
				bl.move(5, 0, z, sp_f)
				while self.servo.areMoving():
					pass
				p += 1
			else:
				p = 0
		t = time()
		sp_f = 100
		sp = 30
		while time() - t <= 2:
			z = -9
			fr.move(5, 0, z, sp_f)
			fl.move(5, 0, z, sp_f)
			mr.move(5, 0, z, sp_f)
			ml.move(5, 0, z, sp_f)
			br.move(5, 0, z, sp_f)
			bl.move(5, 0, z, sp_f)
			while self.servo.areMoving():
				pass
			z = -5
			fr.move(5, 0, z, sp)
			fl.move(5, 0, z, sp)
			mr.move(5, 0, z, sp)
			ml.move(5, 0, z, sp)
			br.move(5, 0, z, sp)
			bl.move(5, 0, z, sp)
			while self.servo.areMoving():
				pass
if __name__ == "__main__":
	from multiservo import Multiservo
	import ik
	def attach_all():
		import json
		with open("/home/pi/pulseWidth.json", "r") as read_file:
			srv = json.load(read_file)
			for i in srv["left"].items():
				for s in i[1]:
					servo.attach(s[0], s[1], s[2])
			for i in srv["right"].items():
				for s in i[1]:
					servo.attach(s[0], s[1], s[2])
	servo = Multiservo()
	fr = ik.leg(servo, 9, 10, 11)
	fl = ik.leg(servo, 0, 1, 2)
	mr = ik.leg(servo, 12, 13, 14, x_offset = 0)
	ml = ik.leg(servo, 3, 4, 5, x_offset = 0)
	br = ik.leg(servo, 15, 16, 17)
	bl = ik.leg(servo, 6, 7, 8)
	do = hexa(servo, fr, fl, mr, ml, br, bl)
	
	attach_all()
	#do.dance()
	#do.go(0, 0, 0, 1)
	while True:
		do.rotate()
	

	
	for i in range(18):
		servo.detach(i)
	
