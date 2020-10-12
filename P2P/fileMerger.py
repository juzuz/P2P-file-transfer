import os

mPath = os.getcwd()
mPath += "/Clients"

def mergeFiles(clientName):
    appendData = ""
    os.chdir(mPath + "/" + str(clientName))
    allFiles = []
    for filename in os.listdir("./"):
        if not filename.endswith(".py") and not filename == "p2p_copied.txt":
            allFiles.append(filename)

    allFiles.sort()
    
    with open("p2p_copied.txt",'w') as outfile:
        for filenames in allFiles:
            with open(filenames) as infile:
                outfile.write(infile.read())

    for files in allFiles:
        os.remove(files)



def main():
    for clients in os.listdir(mPath):
        mergeFiles(clients)

if __name__ == "__main__":
    main()
