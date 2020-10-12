#!/usr/bin/env python3

import socket
from threading import Thread

FILENAME = 'testfile.txt'
PORT = 2680

class ThreadforClient(Thread):
    def __init__(self,conn,addr):
        Thread.__init__(self)
        self.conn = conn
        self.aadr = addr
        print("New Thread started for " +str(addr))

    def run(self):
        f = open(FILENAME,'rb')
        while True:    
            l = f.read(1024)
            while(l):
                self.conn.send(l)
                l = f.read(1024)
            if not l:
                self.conn.close()
                break


# Setting up the socket and binding it to a PORT
# AF_INET is the address family of the socket (IPv4)
# IPv4 expects a tuble of (host,port)
# SOCK_STREAM is for almost always for TCP and SOCK_DGRAM is likely for UDP
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# For multiple connections we need to customize the socket options
# SOL_SOCKET is the level of where the item will be, and the second parameter is the allow
# the use of the same address, so if the connection is terminated and we recall the server code
# we will be able to use the same address.
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('localhost',PORT))
threads = []

while True:
    s.listen(10)
    conn, addr = s.accept()
    # Uses the accepted connection information to start thread
    newThread = ThreadforClient(conn,addr)
    newThread.start()

for t in threads:
    t.join()

