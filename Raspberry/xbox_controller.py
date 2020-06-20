
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
    get = list([304, 305, 308, 307, 315, 158, 317, 318, 310, 311])
class cap:
    x = 16
    y = 17
    RY = 5
    RX = 2
    LX = 0
    LY = 1
    LT = 10
    RT = 9
    get = list([16, 17, 5, 2, 0, 1, 10, 9])

class joy:
    def __init__(self):
        from evdev import InputDevice
        self.ctrl = InputDevice('/dev/input/event0')
        self.vals = list([0] * 18)
        print(self.ctrl)
    def read(self):
        event = self.ctrl.read_one()
        while not event is None:
            print(event.code, event.value)
            event = self.ctrl.read_one()
    def prop(self, x, in_min, in_max, out_min, out_max):
	    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def read(self):
        #from evdev import ecodes
        event = self.ctrl.read_one()
        #print(dir(self.ctrl.read_one()))
        while not event is None:
            code, val, t = event.code, event.value, event.type
            if t == 1 or t == 3 or t == 4:
                #print(event.code, event.value)
                for i in range(len(btn.get)):
                    if code == btn.get[i]:
                        self.vals[i] = val
                for i in range(len(cap.get)):
                    if code == cap.get[i]:
                        self.vals[i + 10] = val
            event = self.ctrl.read_one()
        out = self.vals.copy()
        for i in range(12, 16):
            out[i] = self.prop(self.vals[i], 0, 65535, -2.5, 2.5)
        for i in range(16, 18):
            out[i] = self.prop(self.vals[i], 0, 1023, 3.0, -3.0)
        return out
#[a, b, y, x, options, split, 0, 0, c_x, c_y, l_b, r_b, J_r_y, J_r_x, J_l_x, J_l_y]
if __name__ == "__main__":
    joy = joy()
    from time import sleep
    while True:
        print(joy.read())

        #joy.btn()
        sleep(0.5)
        #print(joy.btn(0))
        #joy.read()
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