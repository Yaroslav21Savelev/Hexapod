import cv2
import numpy as np
import socket

class host:
    def __init__(self, port):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(1)

    def accept(self):
        self.sock.settimeout(99999)
        self.conn, self.addr = self.sock.accept()
        self.conn_f = self.conn.makefile('rb')
        print("Connection library: ip: " + str(self.addr[0]))
        self.data = b' '
        self.sock.settimeout(2)

    def read(self):
        
        while True:
            try:
                self.data += self.conn_f.read(1024)
            except:
                print("Connection library: TimeoutError, reconnecting...")
                self.accept()
                return 0, np.zeros((1, 1))
            first = self.data.find(b'\xff\xd8')
            last = self.data.find(b'\xff\xd9')
            if first != -1 and last != -1:
                jpg = self.data[first:last + 2]
                self.data = self.data[last + 2:]
                return 1, cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

    def write(self, stroke):
        self.conn.send(stroke)

    def close(self):
        self.conn.close()

class client:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.sock = socket.socket()
        self.sock.settimeout(None)
    
    def connect(self):
        try:
            self.sock.connect((self.addr, self.port))
            self.conn = self.sock.makefile('wb')
            self.sock.settimeout(5)
            return 1
        except:
            return 0
    
    def send(self, frame):
        stream = cv2.imencode('.jpg', frame)[1].tostring()
        self.conn.write(stream)
    
    def read(self):
        try:
            data = self.sock.recv(20).decode().lstrip('0')
            return data
        except:
            return None
        
