import Queue
import threading
import json
import config
from util import Utility

class DNSResThread(threading.Thread):
    def __init__(self, conn, response):
        super(DNSResThread, self).__init__()
        self.response = response
        self.conn = conn

    def run(self):
        resQueue = Queue.Queue()
        #a = self.conn.recv(1024)
        while True:
            #Utility.unpackData(self.conn, resQueue)

            while resQueue.empty() == False:
                self.parseResponse(resQueue.get())

    def parseResponse(self,payload):
        response = json.loads(payload)
        # print('this is DNS_Thread')
        # print('response')
        # print(response)
        if response['cmd'] == 'lock':
            print('the leader variable is locked')
        elif response['cmd'] == 'set':
            if response['var'] == 'leader':
                config.setLeader(response['val'])
                print('set leader = '+config.getLeader())
            else:
                self.response.put(payload)
