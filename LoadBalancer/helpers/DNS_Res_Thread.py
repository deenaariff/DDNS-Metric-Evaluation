from util import Utility

class DNSResThread(threading.Thread):
    def __init__(self, conn, response):
        super(DNSREsThread, self).__init__()
        self.response = response
        self.conn = conn
        pass

    def run(self):
        resQueue = Queue.Queue()
        while True:
            Utility.unpackData(self.conn, resQueue)

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
