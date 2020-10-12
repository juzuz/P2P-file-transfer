#!usr/bin/env python3

import socket
import time

PORT = 2680


for i in range(0, 10):
    connid = i+1
    print('Starting connection ', connid)
    s = socket.socket()
    s.connect(('localhost',PORT))
    recieved_f = 'test' + str(connid) +'.txt'
    with open(recieved_f,'wb') as f:
        print("Opened recieving file")
        while True:
            data = s.recv(1024)
            if not data:
                f.close()
                break
            f.write(data)
    f.close()
    s.close()
