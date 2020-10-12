import os
import subprocess

mPath = os.getcwd()
mPath += "/Clients"

numClients =len([file for file in os.listdir(mPath)])
for i in range(1,numClients+1):
    os.chdir(mPath + '/Client' + str(i))
    subprocess.run(['gnome-terminal', '-x',"python3","./client.py","&"])

