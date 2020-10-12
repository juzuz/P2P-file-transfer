import subprocess
import time

subprocess.run(['gnome-terminal', '-x',"python3","./server.py","&"])
time.sleep(5)
subprocess.run(['gnome-terminal', '-x',"python3","./multipleClients.py","&"])
