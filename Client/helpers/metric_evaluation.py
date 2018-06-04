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

class MetricEvaluator:
	
	def __init__(self, commandList):
		self.commandList = commandList 								#Store the command list to reference expected value changes
		self.immediateResponses = [None]*len(commandList)			#For queries made immediately after the store command is sent
		self.postConfirmationResponses = [None]*len(commandList)	#For queries made after the store command returns a response
		
	def recordResponse(self, response):
		correct = response['val'] == self.commandList[response['id']] #Calculate whether the response was correct or not
		responseList = self.immediateResponses if response['preConfirmation'] else self.postConfirmationResponses #Check which list to store the response in
		responseList[response['id']] = (correct, response, time.time()) #Store the result as a tuple of the accuracy, the response itself, and the time returned
	
	def dumpLogs(self):
		#Calculate rate of sucesses and failures for before and after
		numCorrect = 0
		numItems = 0
		for item in self.immediateResponses:
			if item == None:
				continue
			if item[0] == True:
				numCorrect += 1
			numItems += 1
		print "Accuracy of immediate responses: "+(1.0*numCorrect/numItems)
		print "Number of responses: "+numItems+" vs "+len(self.immediateResponses)
		print "\n\n"
		
		numCorrect = 0
		numItems = 0
		for item in self.postConfirmationResponses:
			if item == None:
				continue
			if item[0] == True:
				numCorrect += 1
			numItems += 1
		print "Accuracy of post confirmation responses: "+(1.0*numCorrect/numItems)
		print "Number of responses: "+numItems+" vs "+len(self.postConfirmationResponses)