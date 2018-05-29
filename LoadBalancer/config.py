leader = ''
connDict = {}
ipList = []
numServers = 0
client = None

def setLeader(l):
    global leader
    leader = l

def getLeader():
    global leader
    return leader
