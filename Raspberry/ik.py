from math import *
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(x, min, max):
    if x > max:
        return max
    elif x < min:
        return min
    else:
        return x

class leg():
    def __init__(self, servo, Coxa, Femur, Tibia):
        self.servo = servo
        self.Coxa = Coxa
        self.Femur = Femur
        self.Tibia = Tibia

    def move(self, DestX, DestY, DestZ, speed = 255):
        CoxaL_X = 3
        CoxaL_Y = 0.8
        FemurL = 4.2
        TibiaL = 7.8
        localDestX = sqrt(constrain(sqr(DestX) + sqr(DestY), 0.0, 999999.0)) - CoxaL_X
        CoxaOffset = asin(-CoxaL_Y / (localDestX + CoxaL_X))
        theta = atan2(DestX, DestY) + CoxaOffset

        A = -2 * localDestX
        B = -2 * DestZ
        C = sqr(localDestX) + sqr(DestZ) + sqr(FemurL) - sqr(TibiaL)
        X0 = -A * C / (sqr(A) + sqr(B))
        Z0 = -B * C / (sqr(A) + sqr(B))
        D = sqrt(constrain(sqr(FemurL) - (sqr(C) / (sqr(A) + sqr(B))), 0.0, 999999.0))
        mult = sqrt(constrain(sqr(D) / (sqr(A) + sqr(B)), 0.0, 999999.0))
        ax = X0 + B * mult
        bx = X0 - B * mult
        az = Z0 - A * mult
        bz = Z0 + A * mult
        if (ax < 0):
                ax = 0
                az = -12
        if (bx < 0):
                bx = 0
                bz = -12
        if (az > bz):
                jointLocalX = ax
                jointLocalZ = az
        else:
                jointLocalX = bx
                jointLocalZ = bz
        gama = polarAngle(jointLocalX, jointLocalZ, None)
        alpha = polarAngle(localDestX - jointLocalX, DestZ - jointLocalZ, gama)
        self.servo.write(self.Coxa, int(norm(degrees(theta))), speed)
        self.servo.write(self.Femur, int(norm(degrees(gama))), speed)
        self.servo.write(self.Tibia, int(norm(degrees(alpha))), speed)

def norm(val):
    if val > 180:
        return val - 180
    elif val < 0:
        return val + 180
    else:
        return val

def sqr(val):
    return val * val

def polarAngle(x, y, gama):
    if (gama is None):
        if (x > 0):
            if (y > 0):
                return atan(x / y)
            else:
                return atan(x / y) + pi
        else:
            if(y > 0):
                return 0
            else:
                return pi
    else:
        return gama - (pi / 2 - atan(y / x))


if __name__ == "__main__":
    import multiservo
    import movements
    servo = multiservo.Multiservo()
    do = movements.quadro(servo)
    do.attach_all()
    fr = leg(servo, 11, 10, 9)
    fr.move(5, 4, -6)
