import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
dsp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
width = dsp.width
height = dsp.height
padding = -2
top = padding
bottom = height-padding
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
font = ImageFont.load_default()
dsp.begin()
dsp.clear()
dsp.display()
frame_size = (1280, 720)
frame_center = (frame_size[0] // 2, frame_size[1] // 2)
camera = PiCamera()
camera.resolution = frame_size
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=frame_size)
cascPath = "/home/pi/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
#log.basicConfig(filename='webcam.log',level=log.INFO)
n = 0

for i in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = rawCapture.array
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_180)
    '''
    faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        crop = frame[ y : y + h, x : x + w]
        rszd = cv2.resize(crop, (128, 32), interpolation = cv2.INTER_AREA)
        image = Image.fromarray(rszd).convert("1")
        print("Face detected")
        cv2.imwrite("./faces" + str(n) + ".jpg", crop)
        n += 0
        dsp.image(image)
        dsp.display()
    '''
    print("f")
    rszd = cv2.resize(frame, (128, 32), interpolation = cv2.INTER_AREA)
    image = Image.fromarray(rszd).convert("1")
    dsp.image(image)
    dsp.display()
    
    rawCapture.truncate(0)
