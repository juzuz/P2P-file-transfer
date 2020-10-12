#!usr/bin/env python3
import socket

PORT = 2680


# Setting up the socket and binding it to a PORT
# AF_INET is the address family of the socket (IPv4)
# IPv4 expects a tuble of (host,port)
# SOCK_STREAM is for almost always for TCP and SOCK_DGRAM is likely for UDP
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',PORT))
# File to write transmitted data
recievedF = 'test_copy.txt'
f = open(recievedF,'wb')
# Retrieve the data by chunks of 1024 Bytes
while True:
    data = s.recv(1024)
    # If the data is empty, skip the write and close the file
    if not data:
        f.close()
        break
    f.write(data)
    

print("File retrieved")
s.close()
print("Connection Closed")
