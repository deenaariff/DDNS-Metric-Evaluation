'''

	Author: Vishnu Narayana (file and skeleton code created by Deen Arriff)
	Date: 5/26
	
	This is the main file to run the client-side of the project.
	First, the client calls commandParser to load the test set to use and store it as a list.
	Next, the client calls each command in sequential order. The client will wait for responses.
	Then, the client will record the result by passing it into metric_evaluation.py
	Finally, once all commands are made and responses received, the final metrics will be logged.
	
	
'''


import sys
import socket
import json
import time
from helpers.command_parser import CommandLoader
from helpers.metric_evaluation import UpdatedMetricEvaluator

'''
# Ensure Correct Number of Command Line Args
if len(sys.argv) != 3:
    raise Exception('Not enough arguments. 2 required')
    exit(1)

# Set HOST and PORT INFO
HOST = sys.argv[1]
PORT = int(sys.argv[2])
'''

HOST = 'localhost'
PORT = 5000
commandFile = 'cmds.txt'#raw_input('Please input the command file you would like to parse and run:')
WAIT_TIME = 500.0 #wait time between sends in ms

parser = CommandLoader(commandFile)
#commands = parser.concatCommandsIntoJSON()
metrics = UpdatedMetricEvaluator(parser.getCommandList())

run_client = True  # Run Client in Loop Until User Quits

print "loaded command file"

# New Socket Object

'''
try:
	# Connect to the host and port
	s.connect((HOST, PORT))

# Handle any socket errors
except socket.error as err:
	print err
	exit(1)

except KeyboardInterrupt:
	s.close()
	exit(0)

for query in parser.getCommandList():
	s.send(json.dumps(query))
	if query['cmd'] == 'get':
		response = s.recv(1024)
		metrics.recordResponse(response)

s.close()
'''

def connectAndSendCommand(query, expectResponse):
	s = socket.socket()
	try:
		s = socket.socket()
		print "created socket object"
		# Connect to the host and port
		print "attempting to connect to ", HOST, ":", PORT
		s.connect((HOST, PORT))
		print "sending query"
		s.send(query)
		sendTime = time.time()
		print "sent query"
		if expectResponse:
			response = s.recv(1024)
			responseTime = time.time() - sendTime
			print "response received: "
			print response
			if response:
				metrics.recordResponse(json.loads(response), responseTime)

	# Handle any socket errors
	except socket.error as err:
		print "socket error!"
		print err
		exit(1)

	except KeyboardInterrupt:
		print "keyboard interrupt!"
		s.close()
		exit(0)
	
	print "completed sending query, closing connection"
	s.close()

print "attempting to send commands as json"
for query in parser.getCommandList():
	if 'delay' in query:
		time.sleep(query['delay']/1000.0)
	else:
		connectAndSendCommand(json.dumps(query), query['cmd']=='get' or query['cmd']=='set')
	#time.sleep(WAIT_TIME/1000.0)

metrics.dumpLogs()

'''
#Attempt to send commands
s.send(commands)

#Receive responses from load balancer until it sends the finished signal
while True:
	response = s.recv(1024)
	if response == 'end':
		break
	metrics.recordResponse(response)
	
# Close the socket connection
s.close()
'''
