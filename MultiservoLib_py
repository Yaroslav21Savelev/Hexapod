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
                self.wire = i2c(0)
                self.wire.address(0x47)
                self.valid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                self.min = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                self.max = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                self.pulseWidth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        def attach(self, pin, min = 490, max = 2400):
                self.valid[pin] = 1
                self.min[pin] = min
                self.max[pin] = max

        def detach(self, pin):
                self.writeMicroseconds(pin, 0, 10)
                self.valid[pin] = 0

        def isMoving(self, pin):
                if(self.valid[pin]):
                        self.wire.write(pin)
                        self.wire.write(10 >> 8)
                        self.wire.write(10 & 0xFF)
                        self.wire.write(0 >> 8)
                        self.wire.write(0 & 0xFF)
                        return ord(self.wire.read(1))
                else:
                        return 0

        def waitAll(self):
                for pin in range(0, 18):
                        while self.isMoving(pin):
                                pass

        def attached(self, pin):
                return self.valid[pin]

        def writeMicroseconds(self, pin, pulseWidth, speed = 255):
                if(self.valid[pin]):
                        self.pulseWidth[pin] = pulseWidth
                        self.wire.write(pin)
                        self.wire.write(pulseWidth >> 8)
                        self.wire.write(pulseWidth & 0xFF)
                        self.wire.write(speed >> 8)
                        self.wire.write(speed & 0xFF)

        def write(self, pin, angle, speed = 255):
                if(self.valid[pin]):
                        angle = constrain(angle, 0, 180)
                        pulseWidth = map(angle, 0, 180, self.min[pin], self.max[pin])
                        self.writeMicroseconds(pin, pulseWidth, speed)

        def read(self, pin):
                return map(self.pulseWidth[pin], self.min[pin], self.max[pin], 0, 180)
