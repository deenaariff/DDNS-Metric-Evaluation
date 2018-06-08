import sys
import socket
import json
import time
import Queue
from util import Utility

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


if __name__ == '__main__':
    # Ensure Correct Number of Command Line Args
    if len(sys.argv) < 3:
        #raise Exception(um.NETWORK_ERR)
        exit(1)

    # Set HOST and PORT INFO
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    setDict = {'id':'1','cmd':'set','var':'google.com','val':'129.210.16.90'}
    data = json.dumps(setDict)
    
    s = connectSock(HOST,PORT)
    s.send(data)
    res = s.recv(1024)
    print('message receive for set:',res)
    s.close()

    dict = {'id':'2','cmd':'kill','val':'any'}
    data = json.dumps(dict)
    s = connectSock(HOST,PORT)
    s.send(data)
    response = s.recv(1024)
    s.close()
    print(response)
    
    #for i in range(1,20):
    dict = {'id':'2','cmd':'get','var':'google.com','leader':'True'}
    data = json.dumps(dict)
    s = connectSock(HOST, PORT)
    s.send(data)
    response = s.recv(1024)
    s.close()
    print(response)

    
    dict = {'id':'3','cmd':'get','var':'google.com','leader':'False'}
    data = json.dumps(dict)
    s = connectSock(HOST,PORT)
    s.send(data)
    res = s.recv(1024)
    s.close()
    print(res)
