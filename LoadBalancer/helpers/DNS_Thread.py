import threading
import json
import config
import Queue
from helpers.DNS_Req_Thread import DNSReqThread
from helpers.DNS_Res_Thread import DNSResThread
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
                config.connDict[address[0]] = conn

                print('A node has connected')
                print('Its  IP is ' + address[0]+' Its Port is '+ str(address[1]))

                config.numServers += 1
                config.ipList.append(address)
                #
                # This Thread is used to get response from different server
                responseThread = DNSResThread(conn, self.response)
                responseThread.start()
                # while True:
                #     Utility.unpackData(conn, response)
                #
                #     while response.empty() == False:
                #         self.parseResponse(response.get())
                        #print('current leader = '+config.getLeader())
            except KeyboardInterrupt:
                conn.close()
                break

            conn.close()
