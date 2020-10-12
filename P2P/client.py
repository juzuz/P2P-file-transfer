#!usr/bin/env python3

import socket
from threading import Thread
import time

PORT = 2680

class Client:
    def __init__(self):
        # Create Socket Conenction
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        
        # print
        self.s.connect(('localhost',PORT))
        # Variables to know a clients position within the peers
        self.myIndex = -1
        self.myData = ""
        self.peers = []

        # Setup a thread to listen to the connection requests from peers
        my_ip,my_port = self.s.getsockname()
        lThread = Thread(target=self.listen, args =(my_ip,my_port))
        lThread.start()

        # Sending MSG Threads
        sThread = Thread(target = self.sendMSG)
        sThread.daemon = True
        sThread.start()

        while True:
            data = self.recieveMSG()

            # If the data that was sent is null, this can mean the server disconnected
            if not data:
                print("-" * 10 + "SERVER FAILURE" + "-" * 10)
                break

            # Notifies the index the client is within the peers
            # This is to know which file the client has and which
            # peers it has to ask for the remainding files
            elif data[:1].decode('utf-8') == '\x11':
                self.updateIndex(data[1:].decode('utf-8'))
                
            # When the peers are updated(connect or disconnect)
            # update the clients peer list
            elif data[:1].decode('utf-8') == '\x12':
                self.updatePeers(data[1:].decode('utf-8')[:-1])
                print(str(self.peers))

            # The data recieved is a normal data msg
            else:
                # This is the data that comes from the server
                # It saves the file and to save time, I've set
                # the string as the clients variable data.
                # To further implement p2p, we can change this 
                # So the clients reads the data from it's directory
                self.myData = data.decode('utf-8')
                self.saveFile(data.decode('utf-8'))
                print("\n---FILE FROM SERVER RECIVED---\n")

                # After we recieve the data from the server
                # Call out to each peer in the peer list ex itself
                for i in range(0,len(self.peers)):
                    if i != int(self.myIndex):
                        print("-"*5 + "REQUESTING FILE FROM PEER WITH FILE " + str(i) + "-"*5)
                        self.connectToPeer(self.peers[i].split(',')[0][1:-1],int(self.peers[i].split(',')[1],),i)

    # -------------------------------------
    # Code that takes in the ip and port info 
    # and sets up a connection, as if a server, 
    # to listen to incoming connections
    # ---------------------------------------       
    def listen(self,ip,port):
        ls = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ls.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        print("----CLIENT LISTENING----\n")
        ls.bind((ip,port))
        ls.listen(10)

        while True:
            conn, addr = ls.accept()
            print("<" + str(addr) + "> has connected")
            # After the connection has been made, we create a thread
            # to handle data sending
            sThread = Thread(target=self.sendRequestedFile,args=(conn,addr))
            sThread.start()
        ls.close()
            

    # A method for a thread to communicate with the server.
    def sendMSG(self):
        try:
            sleep(5)
            # After some time(give time so the other clients can connect)
            # A REQ msg will be sent. The server will return the idx of the current 
            # client with respect to the total number of peers 0-onforth
            self.s.send("REQ".encode('utf-8'))
        except KeyboardInterrupt as e:
            self.s.send("DISCONN".encode('utf-8'))
            return

    def recieveMSG(self):
        try:
            data = self.s.recv(1024)
            return data
        except KeyboardInterrupt:
            self.s.send("DISCONN".encode('utf-8'))

    # ----------------------------------------
    # After a connection is established, the client will
    # recieve a idx that specifies the clients position
    # this method will change the current index and send a confirmation
    # ----------------------------------------------
    def updateIndex(self,index):
        self.myIndex = index
        self.s.send("CONFIRM".encode('utf-8'))

    # Update the peer list
    def updatePeers(self,data):
        self.peers = []
        for i in range(0,len(data.split('|'))):
            self.peers.append(data.split('|')[i][1:-1])
        
    # Save a file with the format of (myIndex_sendersIndex)
    def saveFile(self,data,idx = -1):
        if idx == -1:
            f = open("p2p_text_" + self.myIndex + "_"+self.myIndex,"w")
        else:
            f = open("p2p_text_" + self.myIndex + "_"+str(idx),"w")

        f.write(data)
        f.close()


    #---------------------------
    # Establishes a connection to a peer and sends a download request
    # If confirmed, the client will send it's local data and 
    # the file will be saved to the local machine.
    # --------------------------------
    def connectToPeer(self,host,port,idx):
        ds = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ds.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        ds.connect((host,port))

        print("-"*2 + "CLIENT " + self.myIndex + " ESTABLISHED CONNECTION WITH CLIENT " + str(idx) + "-"*2)
        print("-*5" + "SENDING DOWNLOAD REQUEST" + "-" * 5)
        ds.send("DOWNLOAD".encode('utf-8'))

        data = ds.recv(1024).decode('utf-8')
        self.saveFile(data,idx)       
        ds.close()
        print("-"*5 + "FILE P2P_" + self.myIndex + "_" + str(idx) + " HAS BEEN DOWNLOADED" + "-"*5)

    # Send the requested data to the peer        
    def sendRequestedFile(self,conn,addr):
        msg = conn.recv(1024).decode('utf-8')

        if msg == 'DOWNLOAD':
            while self.myData == "":
                continue
            conn.send(self.myData.encode('utf-8'))
        print("-"*5 + "DATA SENT TO PEER" + "-"*5)
        conn.close()


def main():
    Client()


if __name__ == "__main__":
    main()

