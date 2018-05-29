import threading
from helpers.DNS_Req_Thread import DNSReqThread


leader = ''
dict = {}
ipList = []
numServers = 0

class DNSThread(threading.Thread):
    def __init__(self, DNSSock, requests, response):
        super(DNSThread, self).__init__()
        self.resquests = requests
        self.response = response
        self.s = DNSSock


    def run(self):
        # Listen for incoming clients and handle requests
        while True:
            try:
                # conn is a new socket object
                conn, address = self.s.accept()
                while True:
                    payload = conn.recv(100000)

                    if not payload:
                        print("No data Exists")
                    else:
                        print('this is dns thread!')
                        print(payload)
                        self.parseResponse(payload)
                        if self.leader != '':
                            requestThread = DNSReqThread(conn, requests)
                            requestThread.start()

            except KeyboardInterrupt:
                conn.close()
                break

            conn.close()

    def parseResponse(payload):
        global leader
        response = json.load(payload)
        if response['cmd'] == 'lock':
            print('the leader variable is locked')
        elif response['cmd'] == 'set':
            if response['var'] == 'leader':
                leader = response['val']
            else:
                self.response.put(payload)
