import config
import socket
import load_balancer
import json
def setNewDNS(request):
    if config.leader != None:
        s = socket.socket()
        s.connect(config.leader[0], config.leader[1])
        s.send(request)
        response = s.recv(1024)

        if not response:
            print('there is reponse from cluster for set')
            return False
        else:
            config.client.send(response)
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
        if req['leader'] == True
            s.connect(config.leader[0], config.leader[1])
        else:
            index = load_balancer.roundRobin()
            s.connect(config.ipList[index][0], config.ipList[index][1])
        s.send(request)
        response = s.recv(1024)

        if not response:
            print('there is no response from cluster for get')
            return False
        else:
            config.client.send(response)
            s.close()
            config.client.close()
            return True
    except Exception as e:
        print('get IPAddr ',e)
        return False

def setNewLeader(request):
    try:
        req = json.loads(request)
        leaderIP = req['leader_IP']
        leaderPort = req['leader_port']
        config.leader = (leaderIP, leaderPort)
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
        return True
    except Exception as e:
        print('set new Leader',e)
        return False
