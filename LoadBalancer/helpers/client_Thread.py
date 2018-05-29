import threading
from helpers.response_Thread import ResThread


class ClientThread(threading.Thread):
    def __init__(self, sockClient, requests, response):
        super(ClientThread, self).__init__():
        self.s = sockClient
        self.response = response
        self.requests = requests

    def run(self):
        while True:
            try:
                # conn is a new socket object
                conn, address = self.s.accept()

                resThread = ResThread(conn, response)      # new thread for response
                resThread.start()                          # thread start

                payload = conn.recv(100000)
                cmds = []

                if not payload:
                    print ("No data Exists")
                else:
                    print('this is the client thread!')
                    print(payload)
                    self.requests.put(payload)

            except KeyboardInterrupt:
                conn.close()
                break

            conn.close()
