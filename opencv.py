import sys
import cv2 as cv
from cv2 import aruco
import time
import numpy as np
import socket

aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
parameters = aruco.DetectorParameters_create()
cv_file = cv.FileStorage("calib_settings.yaml", cv.FILE_STORAGE_READ)
mtx = cv_file.getNode("camera_matrix").mat()
dist = cv_file.getNode("dist_coeff").mat()
frame_size = [336 / 2, 256 / 2]
cap = cv.VideoCapture(0)

sock = socket.socket()
sock.settimeout(None)
sock.connect(("localhost", 2143))

def sendData(data):
	conn = sock.makefile('wb')
	print(data)
	stream = bytearray()
	stream.append(data >> 8)
	stream.append(data & 0xFF)
	conn.write(stream)
	conn.close()

def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(x, min, max):
        if x > max:
                return max
        elif x < min:
                return min
        else:
                return x
def img():
	global dst
	ret, frame = cap.read()
	dst = getPos(frame, aruco_dict, parameters)

def getPos(frame, aruco_dict, parameters):
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	corners, marker_id, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
	if not(marker_id is None) and not(corners is None):
		if marker_id[0] == 50:
			rect = cv.minAreaRect(corners[0])
			dst = constrain(int(rect[1][0]), 0, 1023)
			marker_center = np.array([int(rect[0][0]),int(rect[0][1])])
			return dst
	return 0

dst = 0

while True:
	img()
	sendData(dst)
	
