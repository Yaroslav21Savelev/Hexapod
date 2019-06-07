import cv2 as cv
from cv2 import aruco

import conLib
try:
        addr = sys.argv[1]
except:
        addr = "192.168.1.123"

session = conLib.client(addr, 4219)
while True:
        if session.connect():
                break
cap = cv.VideoCapture(0)
print(addr)


while True:
        ret, frame = cap.read()
        session.send(frame)
        data = session.read()

