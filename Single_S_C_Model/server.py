#!/usr/bin/env python3
import socket

# Setting up variables and PORT to listen on
FILENAME = 'testfile.txt'
PORT = 2680

# Setting up the socket and binding it to a PORT
# AF_INET is the address family of the socket (IPv4)
# IPv4 expects a tuble of (host,port)
# SOCK_STREAM is for almost always for TCP and SOCK_DGRAM is likely for UDP
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('localhost',PORT))
# Specifies the maximum number of connections allowed
s.listen(10)
conn, addr = s.accept()
print("Connected by, ", addr)

while True:
    # Read the file in binary format
    f = open(FILENAME,'rb')
    l = f.read(1024)
    # Loop until the end of the file is reached
    while(l):
        conn.send(l)
        l = f.read(1024)
    if not l:
        f.close()
        break
# Terminate socket
s.close()