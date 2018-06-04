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
import helpers.command_parser
import helpers.metric_evaluation

# Ensure Correct Number of Command Line Args
if len(sys.argv) < 3:
    raise Exception(um.NETWORK_ERR)
    exit(1)

# Set HOST and PORT INFO
HOST = sys.argv[1]
PORT = int(sys.argv[2])

commandFile = raw_input('Please input the command file you would like to parse and run:')
parser = CommandParser(commandFile)
commands = parser.concatCommandsIntoJSON()
metrics = MetricEvaluator(commands.getCommandList())

run_client = True  # Run Client in Loop Until User Quits


# New Socket Object
s = socket.socket()

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
	s.send(query)
	if query['cmd'] == 'set':
		response = s.recv(1024)
		metrics.recordResponse(response)
		response = s.recv(1024)
		metrics.recordResponse(response)
	else:
		response = s.recv(1024)
		metrics.recordResponse(response)

s.close()

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
