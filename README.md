# P2P-file-transfer
This project is for a networking practice that implements the Server/Client Model.
It begins with code for a connection meant for only one client and server to implementing multithreading techniques to allow multuple clients to connect to th server

The last section is an implementation of a P2P network where the server has a stored file and sends partial pieces to each peer and the peers then communicate with the other peers to get the rest.
The codes is yet to be perfected and there may be some aspects that can be optimized and perfected. 

# How to run the code

## Single_S/C_Model
For the single_S_C_Model, run the server then the client script. The test file will be read, and sent to the client. The server has the file testfile.txt and the client recieves the test_copy.txt. Both files are left in the directories. 

## MultiConnection_S/C
The commands are the same for these scripts. The client script runs multiple threads that acts a connecting client that downloads the file.

## P2P
The P2P file has multiple scripts that faciliate the testing.
python p2p.py will automatically open server.py and multipleClients.py on different terminal tabs and the server will be initiated and the clients in the Clients folder will be proc'd. There can be more clients, but each folder should have the name of Client + "#"

The P2P code is yet completed and does not merge the files after the completion of the download. Run the fileMerger code to merge all the recieved files within each client folder.


