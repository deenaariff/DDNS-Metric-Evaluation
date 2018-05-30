import socket
import select
from collections import deque
import sys

class HermesMQ:

    def __init__(self, async=False, server_address=('localhost', 10000), connections=5):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.async = async

        if async:
            self.server.setblocking(0)

        self.server.bind(server_address)
        self.server.listen(connections)

        if async:
            self.inputs = [self.server]
            self.outputs = []
            self.m_queues = {}
            self.connections = {}
            print "Listening Asychronously to Requests on " + str(server_address[1])
            self.non_blocking_listener()
        else:
            print "Listening Sychronously to Requests on " + str(server_address[1])
            self.blocking_listener()

    def send(self,message,destination):
        if self.async:
            self.async_send(message,destination)
        else:
            sync_send(message,destination)

    def async_send(self, message, destination):
        if destination in self.connections and self.connections[destination]:  # does a valid connection exist ?
            s = self.connections[destination]  # find the existing connection
        else:
            s = socket.socket()
            try:
                s.connect(destination)  # Attempt a connection
                self.connections[destination] = s  # Map destination to connection
                self.m_queues[s] = deque()  # Create a message queue
            except:
                return False

        self.m_queues[s].append(message)  # add the message to be sent
        self.outputs.append(s)  # add this connection to outputs
        return True

    def sync_send(message,destination):
        s = socket.socket()
        try:
            s.connect(destination)  # Attempt a connection
            s.send(message)
        except:
            print "Error occured"
        s.close()

    def blocking_listener(self, handler):

        while True:
            data = self.server.recv(1024)
            if data:
                print "Received data from " + str(_socket.getsockname())
                print "Message: " + data
                handler.handleMessage(data)

        self.server.close()

    def non_blocking_listener(self):

        while True:

            read, write, exceptions = select.select(self.inputs, self.outputs, self.inputs)

            for _socket in read:  # find all sockets that can be read from

                if _socket is self.server:  # we are checking for incoming messages
                    conn, client = _socket.accept()
                    self.connections[client] = conn
                    conn.setblocking(0)  # make sure the connection is non-blocking
                    self.inputs.append(conn)  # we add an established connection to inputs
                    self.m_queues[conn] = deque()

                else:  # we are checking for established connection
                    data = _socket.recv(1024)
                    if data:  # there is data available
                        print "Received data from " + str(_socket.getsockname())
                        print "Message: " + data
                        self.m_queues[_socket].append(data)  # queue the data to be sent
                        if _socket not in self.outputs:
                            self.outputs.append(_socket)
                    else:  # no data -> close the socket
                        if _socket in self.outputs:
                            self.outputs.remove(_socket)
                        self.inputs.remove(_socket)  # remove this socket from inputs
                        _socket.close()
                        del self.m_queues[_socket]

            for _socket in write:  # check for sockets that are writeable

                if socket in self.m_queues and len(self.m_queues[_socket]) > 0:
                    queue = self.m_queues[_socket]  # find the message queue for a connection
                    data = queue.popleft()  # de-queue the data to send
                    try:
                        _socket.send(data)  # send data
                    except:
                        print "Unable to send message back to client " + str(_socket.getsockname())
                else:
                    if _socket in self.outputs:
                        self.outputs.remove(_socket)  # remove socket from outputs

            for _socket in exceptions:  # handle invalid sockets

                self.inputs.remove(_socket)
                if _socket in self.outputs:
                    self.outputs.remove(_socket)
                _socket.close()


if __name__ == "__main__":
    server = HermesMQ(True, ('localhost', int(sys.argv[1])))
    

