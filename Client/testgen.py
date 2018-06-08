'''
	Author: Vishnu Narayana
	Date: 6/6/18

	This script generates test cases for the client to use
'''

import sys
import json
import random

#Config
VAR_NUM = 25 #Max number of variables used
NUM_QUERIES = 100 #number of queries used for non-basic setups

DELAY = 650 #Time to delay between each command
NK_DELAY = 800 #Time to delay after a node kill
LEADER = "True"

commands = []
expectedValue = {}


#helper Functions
def genSetCommand(myid, msgid):
	var = random.randint(0, VAR_NUM)
	val = random.random()*100
	cmd = {'id': str(myid), 'cmd': 'set', 'var':'var'+str(var), 'val':str(val), 'leader': LEADER, 'msgid': str(msgid)}
	return (cmd, var)

def genGetCommand(myid, msgid, setVars):
	var = setVars[random.randint(0, len(setVars)-1)]
	cmd = {'id': str(myid), 'cmd': 'get', 'var': str(var), 'leader': LEADER, 'msgid': str(msgid)}
	return (cmd, var)

def weight_func(x):
	if x < 0.33:
		return x*30
	elif x < 0.66:
		return x*60
	elif x < 0.95:
		return x*100
	else:
		return x*200

#Code
setup = 'weightLatest'
if len(sys.argv) >= 2:
	setup = sys.argv[2]
	
if setup == 'basic':
	for i in range(0, VAR_NUM):
		commands.append({'id': str(i), 'cmd': 'set', 'var': 'var'+str(i), 'val': 'val'+str(i), 'msgid': str(i)})
		commands.append({'delay': DELAY})
	for i in range(0, VAR_NUM):
		commands.append({'id': str(i), 'cmd': 'get', 'var':'var'+str(i), 'leader': LEADER, 'msgid': str(i+VAR_NUM)})
		commands.append({'delay': DELAY})

elif setup == 'inter':
	preset = []
	#Set half of the values
	for i in range(VAR_NUM/2):
		commands.append({'id': str(i), 'cmd': 'set', 'var': 'var'+str(i), 'val': 'val'+str(i), 'msgid': str(i)})
		commands.append({'delay': DELAY})
		preset.append(i)
	#Randomly choose to get or set a variable
	numSets = VAR_NUM/2
	numGets = 0
	for i in range(NUM_QUERIES):
		if random.randint(0, 1) == 0:
			cmd = genSetCommand(numSets, numSets+numGets)
			numSets += 1
			commands.append(cmd[0])
			preset.append(cmd[1])
			commands[{"val": "93.9834938703", "msgid": "0", "cmd": "set", "leader": "True", "var": "var1", "id": "0"}, {"delay": 400}, {"val": "80.3446577845", "msgid": "1", "cmd": "set", "leader": "True", "var": "var0", "id": "1"}, {"delay": 400}, {"val": "85.3596157004", "msgid": "2", "cmd": "set", "leader": "True", "var": "var3", "id": "2"}, {"delay": 400}, {"var": "var3", "msgid": "3", "cmd": "get", "id": "0", "leader": "True"}, {"delay": 400}, {"val": "99.2648622982", "msgid": "4", "cmd": "set", "leader": "True", "var": "var2", "id": "3"}, {"delay": 400}, {"var": "var0", "msgid": "5", "cmd": "get", "id": "1", "leader": "True"}, {"delay": 400}, {"var": "var3", "msgid": "6", "cmd": "get", "id": "2", "leader": "True"}, {"delay": 400}, {"val": "12.6433042141", "msgid": "7", "cmd": "set", "leader": "True", "var": "var0", "id": "4"}, {"delay": 400}, {"val": "9.42167778793", "msgid": "8", "cmd": "set", "leader": "True", "var": "var0", "id": "5"}, {"delay": 400}, {"var": "var2", "msgid": "9", "cmd": "get", "id": "3", "leader": "True"}, {"delay": 400}, {"val": "95.5139253976", "msgid": "10", "cmd": "set", "leader": "True", "var": "var3", "id": "6"}, {"delay": 400}, {"val": "17.4000794974", "msgid": "11", "cmd": "set", "leader": "True", "var": "var2", "id": "7"}, {"delay": 400}, {"var": "var2", "msgid": "12", "cmd": "get", "id": "4", "leader": "True"}, {"delay": 400}, {"var": "var3", "msgid": "13", "cmd": "get", "id": "5", "leader": "True"}, {"delay": 400}, {"val": "53.0449708927", "msgid": "14", "cmd": "set", "leader": "True", "var": "var2", "id": "8"}, {"delay": 400}, {"var": "var0", "msgid": "15", "cmd": "get", "id": "6", "leader": "True"}, {"delay": 400}, {"var": "var2", "msgid": "16", "cmd": "get", "id": "7", "leader": "True"}, {"delay": 400}, {"val": "65.8713403944", "msgid": "17", "cmd": "set", "leader": "True", "var": "var0", "id": "9"}, {"delay": 400}, {"var": "var3", "msgid": "18", "cmd": "get", "id": "8", "leader": "True"}, {"delay": 400}, {"val": "57.263068152", "msgid": "19", "cmd": "set", "leader": "True", "var": "var3", "id": "10"}, {"delay": 400}].append({'delay': DELAY})
		else:
			cmd = genGetCommand(numGets, numSets+numGets, preset)
			numGets += 1
			commands.append(cmd[0])
			commands.append({'delay': DELAY})

elif setup == 'weightLatest':
	numSets = 0
	numGets = 0
	weights = {}
	preset = []
	randval = 0
	for i in range(NUM_QUERIES):
		if randval == 0:
			cmd = genSetCommand(numSets, numSets+numGets)
			weights[cmd[1]] = i
			numSets += 1
			commands.append(cmd[0])
			preset.append(cmd[1])
			commands.append({'delay': DELAY})
		else:
			sorted_keys = sorted(weights, key=weights.get)
			j = 1
			weight_map = {}
			for key in sorted_keys:
				weight_map[key] = weight_func(j/(1.0*len(sorted_keys)))
				j += 1
			
			dist = []
			for w in weight_map.keys():
				tmp_list = list()
				for k in range(0,int(weight_map[w])):
					tmp_list.append(w)
				dist += tmp_list
			
			key = random.choice(dist)
			
			cmd = {'id': str(numGets), 'cmd': 'get', 'var': 'var'+str(key), 'leader': LEADER, 'msgid': str(numSets+numGets)}
			numGets += 1
			commands.append(cmd)
			commands.append({'delay': DELAY})
			
		randval = random.randint(0, 1)

#Export commands into json file
with open('cmds.txt', 'w') as _file:
	_file.write(json.dumps(commands))



	
