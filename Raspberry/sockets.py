import cv2
import numpy as np
import socket

class host:
    def __init__(self, port):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(1)
        #self.sock.setblocking(0)
        self.data = ''

    def accept(self):
        self.sock.settimeout(20)
        try:
            self.conn, self.addr = self.sock.accept()
        except:
            print("Connection timed out")
            from sys import exit
            exit()
        #self.conn.setblocking(0)
        self.conn_f = self.conn.makefile('rb')
        print("Connection library: ip: " + str(self.addr[0]))

    def write(self, frame):
        self.conn.setblocking(1)
        stream = cv2.imencode('.jpg', frame)[1].tostring()
        try:
            self.conn.send(stream)
            #self.conn.send((str(data) + "\n").encode())
        except:
            print("Client shutdown")
            self.conn.close()
            self.accept()
    def read(self):
        self.conn.setblocking(0)
        try:
            self.data += self.conn_f.readline().decode()
            if self.data != "" and self.data.find('\n') != -1:
                s = self.data.strip()
                self.data = ''
                return s
            else:
                return None
        except:
            print("Client shutdown")
            self.conn.close()
            self.accept()
    def close(self):
        self.conn.close()

class client:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.conn = socket.socket()
        self.data = b''

    def connect(self):
        while True:
            try:
                self.conn.connect((self.addr, self.port))
            except:
                pass
            else:
                break
        self.conn_f = self.conn.makefile('rb')
        self.conn.settimeout(None)
        self.conn.setblocking(0)
    def write(self, data):
        try:
            self.conn.send((str(data) + "\n").encode())
        except:
            print("Server shutdown")
            self.conn.close()
            self.connect()
    def read(self):
        #read = self.conn_f.readline()
        while True:
            self.data += self.conn_f.readline()
            first = 0
            last = self.data.find(b'\xff\xd9')
            if last != -1:
                jpg = self.data[first:last + 2]
                self.data = self.data[last + 2:]
                return cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
    def close(self):
        self.conn.close()