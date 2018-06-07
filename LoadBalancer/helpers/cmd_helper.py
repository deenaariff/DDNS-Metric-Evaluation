import config
import socket
import load_balancer
import json
from load_balancer import Algorithm

def setNewDNS(request):
    try:
        if config.leader != None:
            s = socket.socket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((config.leader[0], config.leader[1]))
            config.log(1,"Received SET request: " + request)
            s.send(request+'\n')
            response = s.recv(1024)

            if not response:
                config.log(3,'there is reponse from cluster for set')
                return False
            else:
                config.log(3,response)
                config.log(4,"Sending to Client")
                config.client.send(response)
                return True
        else:
            print('There is no leader now')
            return False
    except Exception as e:
        print('set new DNS ',e)
        return False

def getIPAddr(request, algorithm):
    try:
        response = None
        req = json.loads(request)
        s = socket.socket()
        config.log(1,"Received GET request: " + request)
        if req['leader'] == 'True':
            config.log(2,'sending to leader', config.leader[1]）
            s.connect((config.leader[0], config.leader[1]))
        else:
            index = algorithm.roundRobin()
            config.log(2,'sending to the '+str(index), config.ipList[index])
            s.connect((config.ipList[index][0], config.ipList[index][1]))
            config.log(2,"Sending new Get Request to RAFT")
        s.send(request+'\n')
        response = s.recv(1024)
        config.log(3,'response: ' + response)

        if not response:
            config.log(3,'there is no response from cluster for get')
            return False
        else:
            config.log(4,'SENDING THE RESPONSE BACK TO THE CLIENT')
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
        electionTime = req['election_time']
        if electionTime > config.electionTime:
            config.leader = (leaderIP, leaderPort)
            print('------------------------------------------------')
            print('NEW LEADER DETECTED: '+ str(leaderIP), leaderPort)
            print('------------------------------------------------')
            config.electionTime = electionTime
        return True
    except Exception as e:
        print("ERROR: " + e)
        return False


def killNode(request, algorithm):
    try:
        config.log(1,"Received kill request: " + request)
        req = json.loads(request)
        type = req['val']
        index = algorithm.roundRobin()
        if type != 'any' and type != 'follower':
            return False
        elif type == 'follower':
            while config.ipList[index][1] == config.leader[1]:
                index = algorithm.roundRobin()

        s = socket.socket()
        config.log(2,'Sending KILL message to the '+str(index), config.ipList[index][1])
        s.connect((config.ipList[index][0], config.ipList[index][1]))
        s.send(request+'\n')
        response = s.recv(1024)
        return True
    except Exception as e:
        print(e)
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
