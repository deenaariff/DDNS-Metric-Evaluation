import threading
import json
import config
from helpers.util import Utility

class DNSReqThread(threading.Thread):
    def __init__(self, requests):
        super(DNSReqThread,self).__init__()
        self.requests = requests
        self.numServers = 0
        self.round = -1

    def run(self):
        print("leader is "+config.getLeader())
        while True:
            #print('this is dns req thread!')
            while(self.requests.empty() == False):
                print('this is in the req thread')
                # print(self.requests.get())
                self.sendRequests()




    def sendRequests(self):
        if config.getLeader() == '':
            print('There is no leader')
        else:
            while self.requests.empty() == False:
                request = self.requests.get()
                data = Utility.packData(request)
                obj = json.loads(request)
                if str(obj['leader']) == 'True':
                    leaderIP = str(config.getLeader())
                    conn = config.connDict[leaderIP]
                    conn.send(data)
                else:
                    self.round = self.roundRobin()
                    config.connDict[config.ipList[self.round]].send(data)

    def roundRobin(self):
        if self.round == self.numServers - 1:
            return 0
        else:
            self.round += 1
            return self.round
