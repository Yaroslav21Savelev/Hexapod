# Hexapod

###  Files:
  + source.py - main code file
  + xbox_controlles.py - xbox controller interface
  + multiservo.py - py lib for multiservo board communication via UART
  + ik.py - formules of inverse kinematic
  + movements.py - robot's movements in a cartesian system
  + mpu6050.py - py lib for MPU6050 communication
  + pulseWidth.json - servo configuration file 
  + haarcascade_frontalface_default.xml - Haar cascade
  + lcd_cam.py - test code for drawing PiCamera frames on oled display
  
  #### Add "sudo python3 /home/pi/source.py > /home/pi/startup_log.txt &" to /etc/rc.local
