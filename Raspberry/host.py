import cv2
from sockets import host
cam_session = host(4342)
cam_session.accept()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
size = 5
while True:
    ret, frame = cap.read()
    tmp = cam_session.read()
    if not tmp is None:
        if tmp == "stop":
            break
        size = int(tmp) 
    #frame=cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2GRAY)
    rszd = cv2.resize(frame, (int(len(frame[0]) / size), int(len(frame) / size)), interpolation = cv2.INTER_AREA)
    cam_session.write(rszd)
cap.release()
cam_session.close()