import threading
import json
import config.py
from helpers.DNS_Req_Thread import DNSReqThread



dict = {}
ipList = []
numServers = 0

class DNSThread(threading.Thread):
    def __init__(self, DNSSock, requests, response):
        super(DNSThread, self).__init__()
        self.requests = requests
        self.response = response
        self.s = DNSSock
        self.leader = ''

    def run(self):
        # Listen for incoming clients and handle requests
        while True:
            try:
                # conn is a new socket object
                conn, address = self.s.accept()
                payload = conn.recv(100000)

                if not payload:
                    print("No data Exists")
                else:
                    print('this is dns thread!')
                    print(payload)
                    self.parseResponse(payload)

                    if getLeader() != '':
                        requestThread = DNSReqThread(conn, self.requests, self.dict)
                        requestThread.start()
            except KeyboardInterrupt:
                conn.close()
                break

            conn.close()

    def parseResponse(self,payload):
        response = json.loads(payload)
        if response['cmd'] == 'lock':
            print('the leader variable is locked')
        elif response['cmd'] == 'set':
            if response['var'] == 'leader':
                setLeader(response['val'])
            else:
                self.response.put(payload)
