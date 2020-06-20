import socket
import netifaces
import qrcode
import qrcode.image.svg
from PIL import Image
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=0,
)
class joy:
    def __init__(self, port=9090):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(1)
        self.sock.setblocking(0)
        self.data = b''
        self.vals = list([0] * 18)
        self.cross = [0, 0, 0, 0]
        self.rx = None
        self.port = port

    def getIP(self):
        interfaces = netifaces.interfaces()
        for i in interfaces:
            if i == 'lo':
                continue
            iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
            if iface != None:
                ip = iface[0]['addr']
        return (socket.gethostname(), ip, self.port)

    def info(self, port):
        interfaces = netifaces.interfaces()
        for i in interfaces:
            if i == 'lo':
                continue
            iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
            if iface != None:
                ip = iface[0]['addr']
                ip = "192.168.0.200"
                b = list(map(int, ip.split(".")))
                ip_hex = "AgileTag:"
                for i in b:
                    if i // 16 == 0:
                        ip_hex += "0"
                    ip_hex += hex(i)[2:]
                ip_hex += hex(port)[2:].zfill(4)
                qr.add_data(ip_hex)
                qr.make(fit=True)
                img = qr.make_image()
                img = img.crop((0, 0, 580, 290))
                img = img.resize((128, 32))
                return ip_hex, img

    def connect(self):
        self.sock.settimeout(None)
        self.conn, self.addr = self.sock.accept()
        self.conn.setblocking(0)
        self.rx = self.conn.makefile('rb')
        print("Connection library: ip: " + str(self.addr[0]))
    def read(self):
        return self.vals
    def update(self):
        prop = self.prop
        if self.rx is None:
            return None
        temp = self.rx.read()
        if temp == b'':
            self.close()
            return None
        if not temp is None:
            self.data += temp
            #last = self.data.find(b'eofl')
            out = self.data.decode().split("eofl")
            self.data = b''
            #print(out)

            for packet in out[:-1]:
                packet = list(map(int, packet.split()))
                #print(packet)
                if packet[0] == 20:
                    self.vals[14] = prop(packet[1], 0, 255, 2.5, -2.5)
                    self.vals[15] = prop(packet[2], 0, 255, 2.5, -2.5)
                elif packet[0] == 21:
                    self.vals[12] = prop(packet[2], 0, 255, 2.5, -2.5)
                    self.vals[13] = prop(packet[1], 0, 255, 2.5, -2.5)
                elif packet[0] == 22:
                    self.vals[16] = prop(packet[1], 0, 255, -3, 3)
                elif packet[0] == 23:
                    self.vals[17] = prop(packet[1], 0, 255, -3, 3)
                elif packet[0] == 24:
                    if packet[1] < 4:
                        self.cross[packet[1]] = int(not packet[2])
                        cr = self.cross
                        self.vals[11] = cr[1] - cr[0]
                        self.vals[10] = cr[3] - cr[2]
                    elif 3 < packet[1] < 8:
                        self.vals[packet[1] - 4] = int(not packet[2])
                    elif 7 < packet[1] < 10:
                        self.vals[packet[1] - 2] = packet[2]
                else:
                    print(packet)

        return self.vals

    def prop(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def close(self):
        self.conn.close()



if __name__ == "__main__":
    from time import sleep
    port = 8000
    while True:
        try:
            session = joy(port)
            break
        except:
            port += 1
    _, img = session.info(port)
    print(session.getIP())
    print(_)
    img.save("qrcode.jpg")
    session.connect()
    while True:
        ret = session.update()
        if ret is None:
            print("Reconnecting...")
            tag, img = session.info(port)
            print(tag)
            addr = session.getIP()
            session.connect()
        data = session.read()
        print(data)
        sleep(0.5)
    #['close', 'closed', 'detach', 'fileno', 'flush', 'isatty', 'mode', 'name', 'peek', 'raw', 'read', 'read1', 'readable', 'readinto', 'readinto1', 'readline', 'readlines', 'seek', 'seekable', 'tell', 'truncate', 'writable', 'write', 'writelines']
