'''
	Author: Vishnu Narayana
	Date: 5/26/18
	
	This file takes a file that contains commands and parses them into a serializable format
	
	Command Formats:
		Setting a value: "set variable value leader"
			set- the literal string "set"
			variable- the variable whose value to set
			value- the value to set it to
		
		Getting a value: "get variable leader"
			get- the literal string "get"
			variable- the variable to query
			leader- whether to query the leader only, or a random node
			
			There will be a space between each parameter of the command.
			An id will be assigned to each command when parsing for internal and code based usage
		
'''

import json

class CommandParser:
	
	def __init__(self, file):
		self.cmdList = []
		self.cmdIdSet = 0
		self.cmdIdGet = 0
		cmdFile = open(file)
		for line in cmdFile:
			self._parseLine(line)
		
	def _parseLine(self, line):
		#Check if line is empty
		if line == '' or line == '\n':
			return
			
		#Split the line to parse each part of it
		cmds = line.split()
		leaderCommand = -1
		#Differentiate between set and get, and set up the initial dictionary
		if cmds[0] == 'set':
			leaderCommand = 3
			parsedCommand = {'cmd': 'set', 'var': cmds[1], 'val': cmds[2], 'id': self.cmdIdSet}
			self.cmdIdSet += 1
		elif cmds[0] == 'get':
			leaderCommand = 2
			parsedCommand = {'cmd': 'get', 'var': cmds[1], 'id': self.cmdIdGet, 'leader': True}
			self.cmdIdGet += 1
		else:
			raise ValueError('Improperly formatted command type in text. Must be "get" or "set":\n'+line)
		
		#Parse whether command will query the leader node only or not
		isLeader = True
		if cmds[leaderCommand] == 't' or cmds[leaderCommand] == 'T' or cmds[leaderCommand] == 'true' or cmds[leaderCommand] == 'True':
			isLeader = True
			parsedCommand['leader'] = True
		elif cmds[leaderCommand] == 'f' or cmds[leaderCommand] == 'F' or cmds[leaderCommand] == 'false' or cmds[leaderCommand] == 'False':
			isLeader = False
			parsedCommand['leader'] = False
		else: #Confirm if the value is actually false, and not just bad formatting
			raise ValueError('Improperly formatted boolean value in text:\n'+line)
		
		#Add parsed command list of command
		self.cmdList.append(parsedCommand)
	
	#Takes the internal list of commands and concatenates them into a single json array
	def concatCommandsIntoJSON(self):
		return json.dumps(self.cmdList)
	
	def getCommandList(self):
		return self.cmdList


'''Testing Code: Do not run this file in final product'''
'''
parser = CommandParser('commands.txt')
print parser.concatCommandsIntoJSON()
for item in parser.getCommandList():
	print item
'''