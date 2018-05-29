import threading
import json
import config
import time
from helpers.util import Utility

class DNSReqThread(threading.Thread):
    def __init__(self, requests):
        super(DNSReqThread,self).__init__()
        self.requests = requests
        self.numServers = 0
        self.round = -1

    def run(self):
        #print("leader is "+config.getLeader())
        while True:
            #print('this is dns req thread!')
            while(self.requests.empty() == False):
                print('this is in the req thread')
                self.sendRequests()




    def sendRequests(self):
        if config.getLeader() == '':
            print('There is no leader')
        else:
            while self.requests.empty() == False:
                request = self.requests.get()
                obj = json.loads(request)
                data = Utility.packData(obj)
                
                #print('obj = ')
                #print(obj)
                
                #Load balancer algorithme
                # if leader is True then send to leader
                # if leader is False then send to node determined by round Robin
                
                if str(obj['leader']) == 'True':
                    leaderIP = str(config.getLeader())
                    conn = config.connDict[leaderIP]
                    time.sleep(0.2)
                    conn.send(data)
                else:
                    self.round = self.roundRobin()
                    time.sleep(0.2)
                    config.connDict[config.ipList[self.round]].send(data)

    def roundRobin(self):
        if self.round == self.numServers - 1:
            return 0
        else:
            self.round += 1
            return self.round
