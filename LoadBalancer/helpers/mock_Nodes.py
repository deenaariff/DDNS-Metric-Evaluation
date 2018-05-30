import sys
import socket
import json
import time

def connectSock(HOST, PORT):

    # New Socket Object
    s = socket.socket()
    try:
    	# Connect to the host and port
    	s.connect((HOST, PORT))
        return s
    # Handle any socket errors
    except socket.error as err:
    	print err
    	exit(1)

    except KeyboardInterrupt:
    	s.close()
    	exit(0)

def getServerInfo():
    hostName = socket.getfqdn(socket.gethostname())
    IPAddr = socket.gethostbyname(hostName)
    return IPAddr

if __name__ == '__main__':
    # Ensure Correct Number of Command Line Args
    if len(sys.argv) < 3:
        raise Exception(um.NETWORK_ERR)
        exit(1)

    # Set HOST and PORT INFO
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    s = connectSock(HOST, PORT)
    ip = getServerInfo()

    dict = {'id':1,'cmd':'set','var':'node','val':ip}
    s.send(json.dumps(dict))

    while True:
        
        payload = s.recv(100000)
        if not payload:
            continue
        else:
            print(payload)

    s.close()
