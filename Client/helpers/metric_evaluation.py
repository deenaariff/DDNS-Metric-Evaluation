'''
	Author: Vishnu Narayana
	Date:  5/26/18
	
	This file takes values acquired by the the client from network communication with the load balancer about the result of certain queries.
	Whether the result of the query is what is expected, the metric evaluator will record a success or failure and return a final result.
	
	Required parameters in response object/json:
		val: the value returned by the query
		id: the id of the set value query that this is a response to
		immediate: whether the response was for a query that was made immediately after the set. False for made after a response
'''

import time

'''
	New metric evaluator for changed formats and expected variables.
	Set responses no longer get a response from the load balancer
	Get responses reply with {valid, id, var, val}
		valid: boolean on whether the variable exists on the system yet
		id: id of the get response
		var: variable being queried
		val: value of the variable from the query
'''
class UpdatedMetricEvaluator:
	
	def __init__(self, commandList):
		self.commandList = commandList;
		#Create empty list for responses, length = # of get queries in commandList that match type
		self.responseListSet = [None]*(len([item for item in commandList if 'cmd' in item and item['cmd']=='set']))
		self.responseListGet = [None]*(len([item for item in commandList if 'cmd' in item and item['cmd']=='get']))
		
		#Calculate expected value for each get query
		self.expectedValues = []
		valTable = {}
		for query in commandList:
			if 'cmd' not in query or (query['cmd'] != 'set' and query['cmd'] != 'get'):
				continue
			if query['cmd'] == 'set':
				valTable[query['var']]  = query['val']
			elif query['cmd'] == 'get':
				myval = valTable[query['var']] if query['var'] in valTable else None
				self.expectedValues.append(myval)
		
		#Sanity check to see if # get commands == # matching values in expectedValues
		if len(self.expectedValues) != len(self.responseListGet):
			raise Exception('Number of get queries != length of expectedValues list. Error by client')
	
	def recordResponse(self, response, responseTime):
		#check if response is valid
		if 'cmd' not in response or (response['cmd'] != 'set' and response['cmd'] != 'get'):
			print "ERROR: Invalid response from server! Not a response to a GET or SET query"
			exit(0)
			return
		
		#Get proper list for response
		mylist = None
		if response['cmd'] == 'set':
			mylist = self.responseListSet
		elif response['cmd'] == 'get':
			mylist = self.responseListGet
		
		#Check if response is correct
		resp = None
		if response['valid']:
			resp = response['val']
			
		if response['cmd'] == 'get':
			print 'correctness calc:'
			print 'resp/expected = ', resp, self.expectedValues[int(response['id'])]
			correct = resp == self.expectedValues[int(response['id'])]
		else:
			correct = response['valid']
		mylist[int(response['id'])] = (correct, responseTime, response)
	
	def dumpLogs(self):
		self.calcAccuracy(self.responseListGet)
		self.calcAccuracy(self.responseListSet)
	
	def calcAccuracy(self, _list):
		numCorrect = 0
		numItems = 0
		sumTime = 0
		for item in _list:
			if item == None:
				continue
			if item[0] == True:
				numCorrect += 1
			sumTime += item[1]
			numItems += 1
		if numItems == 0:
			print "No valid responses back!"
			return (0, 0)
		print "Accuracy of immediate responses: "+str(1.0*numCorrect/numItems)
		print "Number of responses: "+str(numItems)+" vs expected responses: "+str(len(_list))
		print "Average time per response: "+str(1000.0*sumTime/numItems)
		print "\n\n"
		
		
		
		return (numCorrect, 1.0*numCorrect/numItems)

class MetricEvaluator:
	
	def __init__(self, commandList):
		self.commandList = commandList 							#Store the command list to reference expected value changes
		numSetCommands = len([item for item in commandList if item['cmd'] == set])
		self.immediateResponses = [None]*numSetCommands			#For queries made immediately after the store command is sent
		self.postConfirmationResponses = [None]*numSetCommands	#For queries made after the store command returns a response
		self.getResponses = [None]*(len(commandList)-numSetCommands)
		
	def recordResponse(self, response):
		correct = response['val'] == self.commandList[response['id']] #Calculate whether the response was correct or not
		responseList = None
		if response['setResponse']:
			responseList = self.immediateResponses if response['preConfirmation'] else self.postConfirmationResponses #Check which list to store the response in
		else:
			responseList = self.getResponses
		if responseList == None:
			raise Exception('Response poorly formatted! setResponse field is not set!')
		
		responseList[response['id']] = (correct, response, time.time()) #Store the result as a tuple of the accuracy, the response itself, and the time returned
	
	def dumpLogs(self):
		#Calculate rate of sucesses and failures for before and after
		calcAccuracy(self.immediateResponses)
		calcAccuracy(self.postConfirmationResponses)
		calcAccuracy(self.getResponses)
	
	def calcAccuracy(self, list):
		numCorrect = 0
		numItems = 0
		for item in list:
			if item == None:
				continue
			if item[0] == True:
				numCorrect += 1
			numItems += 1
		print "Accuracy of immediate responses: "+(1.0*numCorrect/numItems)
		print "Number of responses: "+numItems+" vs "+len(self.immediateResponses)
		print "\n\n"
		return (numCorrect, 1.0*numCorrect/numItems)
