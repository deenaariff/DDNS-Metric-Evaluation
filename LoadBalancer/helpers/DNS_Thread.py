import threading
import json
import config
import Queue
from helpers.DNS_Req_Thread import DNSReqThread
from helpers.util import Utility



dict = {}
ipList = []
numServers = 0

class DNSThread(threading.Thread):
    def __init__(self, DNSSock, requests, response):
        super(DNSThread, self).__init__()
        self.requests = requests
        self.response = response
        self.s = DNSSock

    def run(self):
        # Listen for incoming clients and handle requests
        # if config.getLeader() != '':
        requestThread = DNSReqThread(self.requests)
        requestThread.start()
        while True:
            try:
                # conn is a new socket object
                conn, address = self.s.accept()
                print(conn, address)
                config.numServers += 1
                config.ipList.append(address)
                response = Queue.Queue()
                while True:
                    config.connDict[address[0]] = conn

                    Utility.unpackData(self.s, response)

                    # payload = self.s.recv(100000)
                    # if not payload:
                    #     continue
                    # else:
                    #     print('this is dns thread!')
                    while response.empty() == False:
                        self.parseResponse(response.get())
                        #print('current leader = '+config.getLeader())
                        #config.connDict[address[0]].send('set leader ok!')
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
                config.setLeader(response['val'])
                print('set leader = '+config.getLeader())
            else:
                self.response.put(payload)
