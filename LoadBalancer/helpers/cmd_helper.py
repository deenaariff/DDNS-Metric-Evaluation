import config
import socket
import load_balancer
import json
def setNewDNS(request):
    if config.leader != None:
        s = socket.socket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((config.leader[0], config.leader[1]))
        s.send(request+"\n")
        response = s.recv(1024)

        if not response:
            print('there is reponse from cluster for set')
            return False
        else:
            print('response for set cmd:',response)
            #config.client.send(response)
            s.close()
            config.client.close()
            return True

    else:
        print('There is no leader now')
        return False

def getIPAddr(request):
    try:
        req = json.loads(request)
        s = socket.socket()
        if req['leader'] == 'True':
            s.connect((config.leader[0], config.leader[1]))
        else:
            index = load_balancer.roundRobin()
            #print(config.ipList)
            s.connect((config.ipList[index][0], config.ipList[index][1]))
        s.send(request+'\n')
        response = s.recv(1024)

        if not response:
            print('there is no response from cluster for get')
            return False
        else:
            print(response)
            config.client.send(response)
            return True
    except Exception as e:
        print('get IPAddr ',e)
        return False

def setNewLeader(request):
    try:
        req = json.loads(request)
        leaderIP = req['leader_IP']
        leaderPort = req['leader_port']
        #electionTime = req['electionTime']
        #if electionTime > config.electionTime:
        config.leader = (leaderIP, leaderPort)
        print('here is a new leader'+ str(leaderIP), leaderPort)
        #config.electionTime = electionTime
        return True
    except Exception as e:
        print('set new Leader',e)
        return False

def addNode(request):
    try:
        req = json.loads(request)
        nodeIP = req['node_IP']
        nodePort = req['node_port']
        config.ipList.append(nodeIP, nodePort)
        config.numServers += 1
        print('add a new node',nodeIP, nodePort)
        return True
    except Exception as e:
        print('set new Leader',e)
        return False
