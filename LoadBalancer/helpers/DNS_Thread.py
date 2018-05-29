import threading
import json
import config
import Queue
from helpers.DNS_Req_Thread import DNSReqThread
from helpers.util import Utility

class DNSThread(threading.Thread):
    def __init__(self, DNSSock, requests, response):
        super(DNSThread, self).__init__()
        self.requests = requests
        self.response = response
        self.s = DNSSock

    def run(self):
        requestThread = DNSReqThread(self.requests)
        requestThread.start()
        while True:
            try:
                # conn is a new socket object
                conn, address = self.s.accept()
                print('A node has connected')
                print('Its  IP is ' + address[0]+' Its Port is '+ str(address[1]))
                
                config.numServers += 1
                config.ipList.append(address)
                response = Queue.Queue()
                
                while True:
                    config.connDict[address[0]] = conn

                    Utility.unpackData(conn, response)

                    while response.empty() == False:
                        self.parseResponse(response.get())
                        #print('current leader = '+config.getLeader())
            except KeyboardInterrupt:
                conn.close()
                break

            conn.close()

    def parseResponse(self,payload):
        response = json.loads(payload)
        print('this is DNS_Thread')
        print('response')
        print(response)
        if response['cmd'] == 'lock':
            print('the leader variable is locked')
        elif response['cmd'] == 'set':
            if response['var'] == 'leader':
                config.setLeader(response['val'])
                print('set leader = '+config.getLeader())
            else:
                self.response.put(payload)
