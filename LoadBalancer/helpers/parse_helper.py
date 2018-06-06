import json
import time
import cmd_helper
def parsePayload(payload):
    try:
        message = json.loads(payload)
        cmd = message['cmd']
        if cmd == 'set':
            print('set new DNS pair')
            result = cmd_helper.setNewDNS(payload)
        elif cmd == 'get':
            print('get the IP address')
            result = cmd_helper.getIPAddr(payload)
        elif cmd == 'leader':
            print('this is the new leader')
            result = cmd_helper.setNewLeader(payload)
            print('result'+result)
            print('finish new leader')
        elif cmd == 'node':
            print('this is a new node')
            result = cmd_helper.addNode(payload)
        else:
            return False
        return result
    except Exception as e:
        print('parsePayload', e)
