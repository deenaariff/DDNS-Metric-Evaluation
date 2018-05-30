import socket
from helpers import parse_helper
from helpers import config

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
        s.listen(10)
        print("Server for "+ name +" is running on " + IPAddr)
        print "Server Listening on Port: " + str(s.getsockname()[1])
        return s
    except socket.error as err:
        print "Socket Connection Error %s" % err


def startServer(s):
    while True:
        try:
            # conn is a new socket object
            conn, address = s.accept()

            payload = conn.recv(1024)
            if not payload:
                print('dosen\'t have any payload here')
            else:
                config.client = conn
                parse_helper.parsePayload(payload)
                conn.close()
        except Exception as e:
            print('loadbalancer socket error', e)
            conn.close()
            break
        except KeyboardInterrupt:
            conn.close()
            break
    conn.close()
    s.close()


if __name__ == '__main__':
    IPAddr      = getServerInfo()
    socket      = connectSock(IPAddr, 'Server')
    startServer(socket)
