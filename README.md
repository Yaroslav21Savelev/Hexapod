### Hexapod
#/etc/rc.local
  sudo python3 /home/pi/source.py > /home/pi/startup_log.txt &
### Files:
  source.py - main code file
  xbox_controlles.py - xbox controller interface
  multiservo.py - py lib for multiservo board communication via UART
  ik.py - formules of inverse kinematic
  movements.py - robot's movements in a cartesian system
  
  
