import sys
import socket
import json


def getServerInfo():
    hostName = socket.getfqdn(socket.gethostname())
    IPAddr = socket.gethostbyname(hostName)
    return IPAddr

def sendLeader(HOST, PORT):
    try:
        l = socket.socket()
        l.connect((HOST, PORT))
        dict = {'cmd':'leader','leader_IP': IP, 'leader_port':port}
        data = json.dumps(dict)
        l.send(data)
    except socket.error as e:
        print('send Leader', e)
    finally:
        l.close()

# establish socket connection
def connectSock(IPAddr):

    s = socket.socket()
    # get server host name
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the Socket to localhost at a given port
    try:
        s.bind(('', 0))
        s.listen(1)
        print("Server is running on " + IPAddr)
        print "Server Listening on Port: " + str(s.getsockname()[1])
        return s
    except socket.error as err:
        print "Socket Connection Error %s" % err

if __name__ == '__main__':
    # Ensure Correct Number of Command Line Args
    if len(sys.argv) < 3:
        #raise Exception(um.NETWORK_ERR)
        exit(1)

    # Set HOST and PORT INFO
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    IP = getServerInfo()
    s = connectSock(IP)
    sendLeader(HOST,PORT, IP, s.getsockname()[1])

    while True:
        try:
            request = s.recv(1024)
            req = json.loads(request)
            response = {'id':req['id'],'val':'129.210.16.80'}
            res = json.dumps(response)
            s.send(res)
        except socket.error as e:
            print('leader send response',e)
        finally:
            s.close()
