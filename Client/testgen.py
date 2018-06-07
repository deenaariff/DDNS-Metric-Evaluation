'''
	Author: Vishnu Narayana
	Date: 6/6/18

	This script generates test cases for the client to use
'''

import sys
import json

#Config
VAR_NUM = 100 #Max number of variables used

DELAY = 500 #Time to delay between each command
NK_DELAY = 800 #Time to delay after a node kill

commands = []
expectedValue = {}

setup = 'basic'
if len(sys.argv) >= 2:
	setup = sys.argv[2]
	
if setup == 'basic':
	for i in range(0, VAR_NUM):
		commands.append({'id': i, 'cmd': 'set', 'var': 'var'+str(i), 'val': 'val'+str(i), 'msgid': i})
		commands.append({'delay': DELAY})
	for i in range(0, VAR_NUM):
		commands.append({'id': i, 'cmd': 'get', 'var':'var'+str(i), 'leader': 'True', 'msgid': i+VAR_NUM})
		commands.append({'delay': DELAY})

#Export commands into json file
with open('cmds.txt', 'w') as _file:
	_file.write(json.dumps(commands))