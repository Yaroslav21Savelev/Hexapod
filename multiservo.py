def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(x, min, max):
	if x > max:
		return max
	elif x < min:
		return min
	else:
		return x

import time

class Multiservo:
	def __init__(self):
		from mraa import I2c  as i2c
		import struct
		self.struct = struct
		self.wire = i2c(0)
		self.wire.address(0x47)
		self.valid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.min = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.max = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.pulseWidth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.isStopped =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	def attach(self, pin, min = 490, max = 2400):
		self.valid[pin] = 1
		self.min[pin] = min
		self.max[pin] = max		

	def detach(self, pin):
		self.writeMicroseconds(pin, 0, 10)
		self.valid[pin] = 0

	def isMoving(self, pin):
		if(self.valid[pin]):
			self.wire.writeByte(pin)
			self.wire.writeByte(10 >> 8)
			self.wire.writeByte(10 & 0xFF)
			self.wire.writeByte(0 >> 8)
			self.wire.writeByte(0 & 0xFF)
			b1 = self.wire.read(2)
			b2 = 0
			for b in b1:
        			b2 = b2 * 256 + int(b)
			return b2
		else:
			return 0
	def read(self, pin):
		if(self.valid[pin]):
                        self.wire.writeByte(pin)
                        self.wire.writeByte(15 >> 8)
                        self.wire.writeByte(15 & 0xFF)
                        self.wire.writeByte(0 >> 8)
                        self.wire.writeByte(0 & 0xFF)
                        b1 = self.wire.read(2)
                        b2 = 0
                        for b in b1:
                                b2 = b2 * 256 + int(b)
                        return b2
                else:
                        return 0
	def readMicroseconds(self, pin):
                if(self.valid[pin]):
                        self.wire.writeByte(pin)
                        self.wire.writeByte(20 >> 8)
                        self.wire.writeByte(20 & 0xFF)
                        self.wire.writeByte(0 >> 8)
                        self.wire.writeByte(0 & 0xFF)
                        b1 = self.wire.read(2)
                        b2 = 0
                        for b in b1:
                                b2 = b2 * 256 + int(b)
                        return b2
                else:
                        return 0
	def stop(self, pin):
		if(self.valid[pin] and self.isStopped[pin] == 0):
			pulseWidth = self.readMicroseconds(pin)
			#print(angle)
			self.writeMicroseconds(pin, pulseWidth)
			self.isStopped[pin] = 1
	def areMoving(self):
		for pin in range(0, 18):
			if self.isMoving(pin):
				return 1
		return 0

	def attached(self, pin):
		return self.valid[pin]

	def writeMicroseconds(self, pin, pulseWidth, speed = 255):
		if(self.valid[pin]):
			self.isStopped[pin] = 0
			self.pulseWidth[pin] = pulseWidth
			self.wire.writeByte(pin)
			self.wire.writeByte(pulseWidth >> 8)
			self.wire.writeByte(pulseWidth & 0xFF)	
			self.wire.writeByte(speed >> 8)
			self.wire.writeByte(speed & 0xFF)

	def write(self, pin, angle, speed = 255):
		if(self.valid[pin]):
			angle = constrain(angle, 0, 180)
			pulseWidth = map(angle, 0, 180, self.min[pin], self.max[pin])
			self.writeMicroseconds(pin, pulseWidth, speed)
