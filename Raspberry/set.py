from multiservo import Multiservo
from time import sleep
import movements
servo = Multiservo()
import json
with open("/home/pi/pulseWidth.json", "r") as read_file:
    srv = json.load(read_file)
    for i in srv["left"].items():
        for s in i[1]:
            servo.attach(s[0], s[1], s[2])
    for i in srv["right"].items():
        for s in i[1]:
            servo.attach(s[0], s[1], s[2])
p = 90
servo.write(0, p)
servo.write(9, p)
'''
p = 90
servo.write(1, p)
servo.write(4, p)
servo.write(7, p)
servo.write(10, p)
servo.write(13, p)
servo.write(16, p)
'''
def d():
    for i in range(18):
            servo.detach(i)
#d()