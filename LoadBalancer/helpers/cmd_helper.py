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
            print('SENDING DNS SET TO RAFT')
            s.send(request+'\n')
            response = s.recv(1024)

            if not response:
                print('there is reponse from cluster for set')
                return False
            else:
                print('response for set cmd:',response)
                print('SEND MESSAGE BACK TO CLIENT')
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
        if req['leader'] == 'True':
            print('sending to leader = ',config.leader)
            s.connect((config.leader[0], config.leader[1]))
        else:
            index = algorithm.roundRobin()
            print('sending to the '+str(index) +'machine =', config.ipList[index])
            s.connect((config.ipList[index][0], config.ipList[index][1]))
            print("Sending new Get Request to RAFT")
        s.send(request+'\n')
        response = s.recv(1024)
        print('response ' ,response)

        if not response:
            print('there is no response from cluster for get')
            return False
        else:
            print(response)
            print('SENDING THE RESPONSE BACK TO THE CLIENT')
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
            print(config.leader)
            print('here is a new leader'+ str(leaderIP), leaderPort)
            config.electionTime = electionTime
        return True
    except Exception as e:
        print('set new Leader',e)
        return False


def killNode(request, algorithm):
    try:
        req = json.loads(request)
        type = req['val']
        index = algorithm.roundRobin()
        if type != 'any' and type != 'follower':
            return False
        elif type == 'follower':
            while config.ipList[index][1] == config.leader[1]:
                index = algorithm.roundRobin()

        s = socket.socket()
        print('sending killing message to the '+str(index) +'machine =', config.ipList[index])
        s.connect((config.ipList[index][0], config.ipList[index][1]))
        print('SEND KILLING MESSAGE TO RAFT')
        s.send(request+'\n')
        response = s.recv(1024)
        return True
    except Exception as e:
        print('killing node ',e)
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
