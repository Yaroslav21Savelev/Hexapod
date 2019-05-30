import time
import multiservo
import movements

servo = multiservo.Multiservo()
do = movements.movement(servo)

do.attach_all()
#default()
while True:
        do.forward(50, 10)
