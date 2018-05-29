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

def getServerInfo():
    hostName = socket.getfqdn(socket.gethostname())
    IPAddr = socket.gethostbyname(hostName)
    return IPAddr

if __name__ == '__main__':
    # Ensure Correct Number of Command Line Args
    if len(sys.argv) < 3:
        #raise Exception(um.NETWORK_ERR)
        exit(1)

    # Set HOST and PORT INFO
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    response = Queue.Queue()

    s = connectSock(HOST, PORT)
    ip = getServerInfo()
    
    # prepare for the data
    dict = {'id':1,'cmd':'set','var':'leader','val':ip}
    data = Utility.packData(dict)

    s.send(data)
    
    while True:
        Utility.unpackData(s, response)
        while response.empty() == False:
            obj = response.get()
            #print('this is mock_dns')
            #print('obj')
            #print(obj)
            request = json.loads(obj)
            # prepare the response
            res= {'id':str(request['id']),'cmd':'set','var':str(request['var']),'val':str(request['id'])}
            d = Utility.packData(res)
            time.sleep(0.2)
            s.send(d)
    s.close()
