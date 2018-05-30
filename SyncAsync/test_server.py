import sys
import socket

def send(message,destination):
    s = socket.socket()
    try:
        s.connect(destination)  # Attempt a connection
        s.send(message)
    except:
        print "Error occured"
    s.close()


if __name__ == "__main__":
	send("test",('localhost',int(sys.argv[1])))