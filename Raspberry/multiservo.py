
def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(x, min, max):
	if x > max:
		return max
	elif x < min:
		return min
	else:
		return x

class Multiservo:
    def __init__(self):
        from serial import Serial
        self.wire = Serial("/dev/serial0", 57600, timeout=1)
        #from time import sleep
        #self.sleep = sleep
        self.addr = 0x47
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
            self.wire.write(bytes([pin]))
            self.wire.write(bytes([10 >> 8]))
            self.wire.write(bytes([10 & 0xFF]))
            self.wire.write(bytes([0 >> 8]))
            self.wire.write(bytes([0 & 0xFF]))
            
            b1 = self.wire.read()[0]
            b2 = self.wire.read()[0]
            out = b1 * 256 + b2
            return out
        else:
            return 0
    def read(self, pin):
        out = self.readMicroseconds(pin)
        if out is None:
            return None
        else:
            out = round(map(out, self.min[pin], self.max[pin], 0, 180))
            return out
    def readMicroseconds(self, pin):
        if(self.valid[pin]):
            self.wire.write(bytes([pin]))
            self.wire.write(bytes([20 >> 8]))
            self.wire.write(bytes([20 & 0xFF]))
            self.wire.write(bytes([0 >> 8]))
            self.wire.write(bytes([0 & 0xFF]))
            b1 = self.wire.read()[0]
            b2 = self.wire.read()[0]
            out = b1 * 256 + b2
            return out
        else:
            return None
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
    '''
    def writeMicroseconds(self, pin, pulseWidth, speed = 255):
        if(self.valid[pin]):
            self.isStopped[pin] = 0
            self.pulseWidth[pin] = pulseWidth
            self.wire.write_block_data(pin, [int(pulseWidth) >> 8, int(pulseWidth) & 0xFF, int(speed) >> 8, int(speed) & 0xFF])
    '''
    def wr(self, msg):
        self.wire.write(msg)
    def writeMicroseconds(self, pin, pulseWidth, speed = 255):
        if(self.valid[pin]):
            self.isStopped[pin] = 0
            self.pulseWidth[pin] = pulseWidth
            self.wire.write(bytes([pin]))
            self.wire.write(bytes([int(pulseWidth) >> 8]))
            self.wire.write(bytes([int(pulseWidth) & 0xFF]))	
            self.wire.write(bytes([int(speed) >> 8]))
            self.wire.write(bytes([int(speed) & 0xFF]))

    def write(self, pin, angle, speed = 255):
        if(self.valid[pin]):
            angle = constrain(angle, 0, 180)
            pulseWidth = map(angle, 0, 180, self.min[pin], self.max[pin])
            self.writeMicroseconds(pin, pulseWidth, speed)

if __name__ == "__main__":
    servo = Multiservo()
    servo.attach(2)
    servo.write(2, 120, 5)
    for i in range(300):
        servo.isMoving(2)
    print("end")