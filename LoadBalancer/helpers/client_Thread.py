import threading
import socket
import config
from helpers.client_Res_Thread import ResThread
from helpers.util import Utility


class ClientThread(threading.Thread):
    def __init__(self, sockClient, requests, response):
        super(ClientThread, self).__init__()
        self.s = sockClient
        self.response = response
        self.requests = requests

    def run(self):
        resThread = ResThread(self.response)      # new thread for response
        resThread.start()                          # thread start
        while True:
            try:
                # conn is a new socket object
                conn, address = self.s.accept()
                config.client = conn

                while True:
                    Utility.unpackData(conn, self.requests)

            except socket.error as e:
                print('client Thread ', e)
            except KeyboardInterrupt:
                conn.close()
                break

            conn.close()
