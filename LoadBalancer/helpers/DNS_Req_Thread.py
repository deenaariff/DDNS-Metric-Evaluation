import threading
import config.py

class DNSReqThread(threading.Thread):
    def __init__(self, conn, requests):
        super(DNSReqThread,self).__init__()
        self.requests = requests
        self.numServers = 0
        self.round = 0

    def run(self):
        while True:
            #global leader
            print('leader is '+ getLeader())
            #print('this is dns req thread!')
            while(self.requests.empty() == False):
                print('this is in the req thread')
                print(self.requests.get())
                # self.sendRequests()




    # def sendRequests():
    #     if self.dict['leader'] == '':
    #         print('There is no leader')
    #     else:
    #         while self.request is not empty:
    #             if request['leader'] == True:
    #                 self.dict[self.leader].send(request)
    #             else:
    #                 self.dict[self.ipList[self.round]].send(request)
    #
    # def roundRobin():
    #     if self.round == self.numServers - 1:
    #         return 0
    #     else:
    #         self.round += 1
    #         return self.round
