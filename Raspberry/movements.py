class quadro():
	def __init__(self, servo):
		self.m = [[2, 11, 8, 17], [1, 10, 7, 16], [0, 9, 6, 15]]
		self.pos = 0
		self.servo = servo
		
	def attach_all(self):
		servo = self.servo
		m = self.m
		servo.attach(m[0][0], 750, 2490)
		servo.attach(m[0][1], 730, 2550)
		servo.attach(m[0][2], 550, 2370)
		servo.attach(m[0][3], 720, 2500)
		
		servo.attach(m[1][0], 600, 2450)
		servo.attach(m[1][1], 700, 2430)
		servo.attach(m[1][2], 710, 2640)
		servo.attach(m[1][3], 700, 2550)

		servo.attach(m[2][0], 620, 2300)
		servo.attach(m[2][1], 700, 2550)
		servo.attach(m[2][2], 730, 2550)
		servo.attach(m[2][3], 730, 2550)
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

	def go(self, dir, speed_1, height):
		if dir:
			dp = -50
		else:
			dp = 50
		m = self.m
		servo = self.servo
		speed_2 = 255
		height_1 = self.constrain(height, 0, 155) + 25
		height_2 = self.constrain(height, 25, 180) - 25
		if(servo.areMoving()):
			return
		elif self.pos == 0:
			servo.write(m[1][0], height_2, speed_2)
			servo.write(m[2][0], height_2, speed_2)
			servo.write(m[1][3], height_2, speed_2)
			servo.write(m[2][3], height_2, speed_2)
		elif self.pos == 1:
			servo.write(m[0][0], 110 + dp, speed_2)
			servo.write(m[0][3], 50 + dp, speed_2)
		elif self.pos  == 2:
			servo.write(m[1][0], height_1, speed_2)
			servo.write(m[2][0], height_1, speed_2)
			servo.write(m[1][3], height_1, speed_2)
			servo.write(m[2][3], height_1, speed_2)
		elif self.pos == 3:
			servo.write(m[0][0], 110, speed_1)
			servo.write(m[0][1], 110 - dp, speed_1)
			servo.write(m[0][2], 50 - dp, speed_1)
			servo.write(m[0][3], 50, speed_1)
		elif self.pos == 4:
			servo.write(m[1][1], height_2, speed_2)
			servo.write(m[2][1], height_2, speed_2)
			servo.write(m[1][2], height_2, speed_2)
			servo.write(m[2][2], height_2, speed_2)
		elif self.pos == 5:
			servo.write(m[0][1], 110 + dp, speed_2)
			servo.write(m[0][2], 50 + dp, speed_2)
		elif self.pos == 6:
			servo.write(m[1][1], height_1, speed_2)
			servo.write(m[2][1], height_1, speed_2)
			servo.write(m[1][2], height_1, speed_2)
			servo.write(m[2][2], height_1, speed_2)
		elif self.pos == 7:
			servo.write(m[0][0], 110 - dp, speed_1)
			servo.write(m[0][1], 110, speed_1)
			servo.write(m[0][2], 50, speed_1)
			servo.write(m[0][3], 50 - dp, speed_1)
		else:
			self.pos = 0
			return
		self.pos += 1

	def rotate(self, dir, speed_1, height):
		m = self.m
		if dir:
			dp = -20
		else:
			dp = 20
		servo = self.servo
		speed_2 = 255
		height_1 = self.constrain(height, 0, 155) + 25
		height_2 = self.constrain(height, 25, 180) - 25
		if servo.areMoving():
			return
		if self.pos == 0:
			servo.write(m[1][0], height_2, speed_2)
			servo.write(m[2][0], height_2, speed_2)
			servo.write(m[1][3], height_2, speed_2)
			servo.write(m[2][3], height_2, speed_2)
		elif self.pos == 1:
			servo.write(m[0][0], 50 + dp, speed_2)
			servo.write(m[0][3], 50 - dp, speed_2)
		elif self.pos == 2:
			servo.write(m[1][0], height_1, speed_2)
			servo.write(m[2][0], height_1, speed_2)
			servo.write(m[1][3], height_1, speed_2)
			servo.write(m[2][3], height_1, speed_2)
		elif self.pos == 3:
			servo.write(m[1][1], height_2, speed_2)
			servo.write(m[2][1], height_2, speed_2)
			servo.write(m[1][2], height_2, speed_2)
			servo.write(m[2][2], height_2, speed_2)
		elif self.pos == 4:
			servo.write(m[0][1], 50 - dp, speed_2)
			servo.write(m[0][2], 50 + dp, speed_2)
		elif self.pos == 5:
			servo.write(m[1][1], height_1, speed_2)
			servo.write(m[2][1], height_1, speed_2)
			servo.write(m[1][2], height_1, speed_2)
			servo.write(m[2][2], height_1, speed_2)
		elif self.pos == 6:
			servo.write(m[0][0], 50 - dp, speed_1)
			servo.write(m[0][1], 50 + dp, speed_1)
			servo.write(m[0][2], 50 - dp, speed_1)
			servo.write(m[0][3], 50 + dp, speed_1)
		else:
			self.pos = 0
			return
		self.pos += 1	
