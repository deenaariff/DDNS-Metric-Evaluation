import socket
import threading
import Queue
from helpers.DNS_Thread import DNSThread
from helpers.client_Thread import ClientThread

# one thread is used to connect with client
# anther thread is used to connect with the DNS cluster

# get the IPAddr of the Server
def getServerInfo():
    hostName = socket.getfqdn(socket.gethostname())
    IPAddr = socket.gethostbyname(hostName)
    return IPAddr


# establish socket connection
def connectSock(IPAddr, name):
    s = socket.socket()
    # get server host name
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the Socket to localhost at a given port
    try:
        s.bind(('', 0))
        print("Server for "+ name +" is running on " + IPAddr)
        print "Server Listening on Port: " + str(s.getsockname()[1])
        return s
    except socket.error as err:
        print "Socket Connection Error %s" % err



if __name__ == '__main__':
    IPAddr      = getServerInfo()
    sockClient  = connectSock(IPAddr, 'client')
    print()
    sockDNS     = connectSock(IPAddr, 'DNS servers')
    
    sockClient.listen(1)
    sockDNS.listen(10)

    requests    = Queue.Queue()
    response    = Queue.Queue()
    clientThread    = ClientThread(sockClient, requests, response)
    DNSThread       = DNSThread(sockDNS, requests,response)

    clientThread.start()
    DNSThread.start()
