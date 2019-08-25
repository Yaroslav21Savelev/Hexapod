import socket

class host:
    def __init__(self, port):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(1)
        self.sock.setblocking(0)
        self.data = ''

    def accept(self):
        self.sock.settimeout(None)
        self.conn, self.addr = self.sock.accept()
        self.conn_f = self.conn.makefile('rb')
        print("Connection library: ip: " + str(self.addr[0]))

    def read(self):
        self.data += self.conn_f.readline().decode()
        if self.data != "" and self.data.find('\n') != -1:
            s = self.data.strip()
            self.data = ''
            return s
        else:
            return None


    def write(self, data):
        try:
            self.conn.send((str(data) + "\n").encode())
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
        self.data = ''

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

    def read(self):
        self.data += self.conn_f.readline().decode()
        if self.data != "" and self.data.find('\n') != -1:
            s = self.data.strip()
            self.data = ''
            return s
        else:
            return None


    def write(self, data):
        try:
            self.conn.send((str(data) + "\n").encode())
        except:
            print("Client shutdown")
            self.conn.close()
            self.connect()

    def close(self):
        self.conn.close()