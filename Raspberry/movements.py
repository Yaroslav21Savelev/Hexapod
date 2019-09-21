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

	def agile(self, x, y, z):
		fr = self.fr
		fl = self.fl
		mr = self.mr
		ml = self.ml
		br = self.br
		bl = self.bl
		x_ = 6
		fr.move(x_ - x, 3 + y, -7 + z, 60)
		fl.move(x_ + x, 3 + y, -7 + z, 60)
		mr.move(x_ - x, 0 + y, -7 + z, 60)
		ml.move(x_ + x, 0 + y, -7 + z, 60)
		br.move(x_ - x, -3 + y, -7 + z, 60)
		bl.move(x_ + x, -3 + y, -7 + z, 60)

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
		mr.move(x_ - 0.5, 0 , start + x, 60)
		ml.move(x_ - 0.5, 0 , start - x, 60)
		br.move(x_, -2 , start + y + x, 60)
		bl.move(x_, -2 , start + y - x, 60)
if __name__ == "__main__":
	from multiservo import Multiservo
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
	attach_all()
	p = 90
	servo.write(1, p)
	servo.write(4, p)
	servo.write(7, p)

	p = 180
	servo.write(2, p)
	servo.write(5, p)
	servo.write(8, p)
