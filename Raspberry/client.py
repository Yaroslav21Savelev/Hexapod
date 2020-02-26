import cv2
from sockets import client
addr = "172.20.10.14"
#addr = "192.168.0.200"
print(addr)
cap = client(addr, 4342)
cap.connect()
size = 5
cap.write(size)

def on_trackbar(val):
    global size
    size = val + 1
    cap.write(size)

cv2.namedWindow("Camera")
cv2.createTrackbar("Res", "Camera", 4, 19, on_trackbar)

while True:
    frame = cap.read()
    rszd = cv2.resize(frame, (int(len(frame[0]) * size / 2), int(len(frame) * size / 2)), interpolation = cv2.INTER_AREA)
    cv2.imshow('Camera', rszd)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cap.write("stop")
        break
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.close()