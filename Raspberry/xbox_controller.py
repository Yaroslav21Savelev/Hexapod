
class btn:
    a = 304
    b = 305
    y = 308
    x = 307
    menu = 315
    split = 158
    L = 317
    R = 318
    LB = 310
    RB = 311
class cap:
    x = 16
    y = 17
    RY = 5
    RX = 2
    LX = 0
    LY = 1
    LT = 10
    RT = 9

class joy:
    def __init__(self):
        from evdev import InputDevice
        self.ctrl = InputDevice('/dev/input/event1')
        print(self.ctrl)
    def read(self):
        event = self.ctrl.read_one()
        while not event is None:
            if event.code == 5:
                print(event.code, event.value)
            event = self.ctrl.read_one()
    def prop(self, x, in_min, in_max, out_min, out_max):
	    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    def update(self, x, y, z, mode):
        event = self.ctrl.read_one()
        while not event is None:
            #print(event.code, event.value)
            
            code, val = event.code, event.value
            if code == btn.x and val:
                mode = 10
            elif code == btn.y and val:
                mode = 1
            elif code == btn.a and val:
                mode = 3
            elif code == btn.split and val:
                mode = 2
            elif code == btn.LB and val:
                mode = 30
            elif code == btn.RB and val:
                mode = 31
            elif code == cap.y and val == -1:
                mode = 35
            elif code == cap.y and val:
                mode = 36
            elif code == cap.RX:
                x = self.prop(val, 0, 65535, -2.5, 2.5)
            elif code == cap.RY:
                y = self.prop(val, 0, 65535, -2.5, 2.5)
            elif code == cap.RT:
                z = self.prop(val, 0, 1023, 3.0, -3.0)
            elif code == btn.menu and val:
                mode = 25
                return x, y, z, mode
            event = self.ctrl.read_one()
        return x, y, z, mode
        
    
if __name__ == "__main__":
    joy = joy()
    while True:
        joy.read()
        #x, y, z, mode = joy.update(0, 0, 0, 0)

'''
for event in joy.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            if event.code == btn.a:
                print("A")
            elif event.code == btn.b:
                print("B")
'''