#!/usr/bin/env python3

import socket
import sys
from threading import Thread
import os
import re
from math import floor

FILENAME = "testfile.txt"
PORT = 2680

class Server:
    # Establish socket connection
    def __init__(self,file):
        try:
            self.file = file
            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.connections = []
            self.peers = []

            self.s.bind(('localhost',PORT))
            self.s.listen(1)
            print("-" * 10 + "Server running" + "-" * 10)
            self.run()
        except Exception as e:
            sys.exit()

    # Run a handler thread that handles the request of clients
    # Update the peers and conncetion info and send it to the clients
    def run(self): 
        while True:
            conn, addr = self.s.accept()
            self.peers.append(addr)
            print("The current peers are : {}".format(self.peers))
            hThread = Thread(target = self.handler, args =(conn,addr))
            hThread.daemon = True
            hThread.start()
            self.connections.append(conn)
            print("{}, connected)".format(addr))
            print("-"*30)
            self.sendPeers()

           
    # The handler recieves information from the clients and acts accordingly
    def handler(self,conn,addr):
        try:
            while True:
                data = conn.recv(1024)
                # Disconnection Request removes from peer and connections
                if data and data.decode('utf-8') == 'DISCONN':
                    self.disconnect(conn,addr)
                
                #The REQ request is for the data sending
                elif data and data.decode('utf-8') == 'REQ':
                    # We divide the file into chunks according to the number of connections
                    # Then send the respective chunk to the client
                    # The current problem with this method is when the size of the chunk
                    # is larger than 1024. We can change the send to a while loop
                    # to make sure that all of the data is sent.
                    # Another way to improve is to have data on the bandwith, so a client
                    # with a larger bandwidth can recieve more bytes.
                    # This way the file size is dynamical and will be able to maximize the downlaod speed
                    num_conn = len(self.connections)
                    chunk_size = floor(os.path.getsize(FILENAME)/num_conn)
                    chunk_index = self.connections.index(conn)
                    # Send a "\x11" to specify that this is the clients idx
                    conn.send(b'\x11' + bytes(str(chunk_index),'utf-8'))
                    
                    # Once the client confirms it's idx we send the information
                    response = conn.recv(1024).decode('utf-8')
                    if response == "CONFIRM":
                        print("-"*5 + "SENDING FILE" + "-" *5)
                        if chunk_index == num_conn-1:
                            conn.send(self.file[chunk_size * chunk_index:])
                        else :
                            conn.send(self.file[chunk_size * chunk_index: chunk_size * (chunk_index+1)])                    
        except Exception as e:
            sys.exit()

    # A method that sends the peer information to everyone connected
    def sendPeers(self):
        peer_list = ""

        for connection in self.connections:
            peer_list += re.search("raddr=((.*))>",str(connection)).group(1) + "|"

        for connection in self.connections:
            connection.send(b'\x12' + bytes(peer_list,"utf-8"))

    # Disconnects a peer
    def disconnect(self,conn,addr):
        self.connections.remove(conn)
        self.peers.remove(addr)
        conn.close()
        self.sendPeers()
        print("{} , disconnected".format(addr))
        print("-" * 30)


52
def convert_to_bytes(file_name):
    file = open(file_name,'r')
    read_data = file.read()
    return read_data.encode('utf-8')


def main():
    while True: 
        try:
            Server(convert_to_bytes(FILENAME))

        except KeyboardInterrupt:
            sys.exit()
  


if __name__ == "__main__":
    main()
