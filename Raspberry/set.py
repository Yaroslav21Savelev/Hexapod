import multiservo
import movements
servo = multiservo.Multiservo()
from time import sleep
do = movements.quadro(servo)
do.attach_all()

'''
while True:
	for i in range(180):
		for j in range(18):
			servo.write(j, i)
		time.sleep(0.01)
	for i in range(180, 0):
        	for j in range(18):
        	        servo.write(j, i)
	        time.sleep(0.01)


for i in [0, 1, 9, 10, 15, 16, 6, 7]:
	servo.write(i, 0)
'''
#servo.write(11, 20, 5)
#print("isMoving", servo.readMicroseconds(11))

servo.write(10, 120, 5)
#print("isMoving", servo.isMoving(1))

for i in range(300):
	print(servo.isMoving(10))
	print(servo.readMicroseconds(10))
	#sleep(0.05)
	#servo.write(10, 80, 5)
