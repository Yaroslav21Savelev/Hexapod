# Hexapod
### Show.pptx - main presentation
### [Controller app for android](https://drive.google.com/file/d/1xm58UqlrQnhqSUL2H1lBoyYgTHVY_Xh2/view?usp=sharing)
##  Raspberry Pi files:
  + source.py - main code file
  + app_controller.py - android app controller interface
  + multiservo.py - py lib for multiservo board communication via UART
  + ik.py - formules of inverse kinematics
  + movements.py - robot's movements in a cartesian system
  + mpu6050.py - py lib for MPU6050 communication
  + pulseWidth.json - servos configuration file 
  + haarcascade_frontalface_default.xml - Haar cascade
  + lcd_cam.py - test code for drawing PiCamera frames on oled display
  + source_xbox.py - old main code file with xbox one controller support
  + xbox_controller.py - xbox controller interface
##  SolidWorks files:
  + AGILE_assem - full assembly of robot
## Other files:
  + MS_board.ino - code for multiservo ATmega 2560 based board
  + MS_board.lay6 - SprintLayout file, multiservo board layout
#### config RasPi
    chmod +x source.py
    Add "sudo python3 /home/pi/source.py > /home/pi/startup_log.txt &" to /etc/rc.local
#### installing i2c dislpay lib
    sudo apt-get update
    sudo apt-get install build-essential python-pip python-dev python-smbus git
    git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
    cd Adafruit_Python_GPIO
    sudo python3 setup.py install
    cd ..
    git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
    cd Adafruit_Python_SSD1306
    sudo python3 setup.py install
    cd ..
#### config joy (not important for android controller app)
    sudo apt-get install xboxdrv
    echo 'options bluetooth disable_ertm=Y' | sudo tee -a /etc/modprobe.d/bluetooth.conf
    sudo reboot
    sudo bluetoothctl
###### in bluetoothctl term
    agent on
    default-agent
    scan on
    connect [MAC]

# materials
  + https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/
  + https://rf2035.net/labs/faculty/1/lab/8/
