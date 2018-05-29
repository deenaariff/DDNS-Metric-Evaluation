import sys
import socket
import json
import time
import Queue

from helpers.util import Utility
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
        raise Exception(um.NETWORK_ERR)
        exit(1)

    # Set HOST and PORT INFO
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    s = connectSock(HOST, PORT)
    response = Queue.Queue()
    for i in range(1,20):
        dict = {'id':i,'cmd':'set','var':'google.com','val':'123.223.323.423','leader':'True'}
        data = Utility.packData(dict)
        s.send(data)

    while True:
        Utility.unpackData(s, response)
        while response.empty() == False :
            print(response.get())
    s.close()
