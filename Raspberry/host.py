import cv2
from sockets import host
from picamera.array import PiRGBArray
from picamera import PiCamera
print("Starting stream")
cam_session = host(4342)
cam_session.accept()
'''
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
'''
size = 5

frame_size = (1280, 720)
frame_center = (frame_size[0] // 2, frame_size[1] // 2)
camera = PiCamera()
camera.resolution = frame_size
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=frame_size)
try:
    for i in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = rawCapture.array
        frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_180)
        frame = cv2.circle(frame, frame_center, 15, (0, 0, 255), 8) 
        #ret, frame = cap.read()
        tmp = cam_session.read()
        if not tmp is None:
            if tmp == "stop":
                break
            size = int(tmp) 
        #frame=cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2GRAY)
        rszd = cv2.resize(frame, (int(len(frame[0]) / size), int(len(frame) / size)), interpolation = cv2.INTER_AREA)
        cam_session.write(rszd)
        rawCapture.truncate(0)
except Exception as e:
    print(e)
    print("Closing session")
    cam_session.close()
    print("Closing camera")
    camera.close()

cam_session.close()
camera.close()
