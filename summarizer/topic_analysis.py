# Simple program that demonstrates how to invoke Azure ML Text Analytics API: topic detection.
import httplib
import urllib
import sys
import base64
import json
import time
import os
import math
import hashlib

# memoize previous searches for runtime
memoized = {}

def get_header():
	# read key from file
	account_key = ''

	with open('summarizer/azure_key.txt') as file:
		account_key = file.readline().strip()

	headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
	return headers


def get_list_of_blocks(file_name):
	# Path to file with JSON inputs.
	f = open(file_name, 'r')
	#for line in f:
	#	print(line)
	files = []

	#TODO: check "rounding"
	x = int(math.ceil(os.stat(file_name).st_size/5000.0))
	print x
	for block in xrange(x):
		lines = f.readline(5000)
		modFileName = str(block) + file_name
		with open(modFileName, 'a+') as temp:
			#sprint sys.getsizeof(lines)
			for line in lines:
				#print line
				temp.write(line)
			files.append(temp)
	f.close()
	return files

#some shit
"""obj = json.loads(result)
for keyphrase_analysis in obj['documents']:
	print('Key phrases ' + str(keyphrase_analysis['id']) + ': ' + ', '.join(map(str,keyphrase_analysis['keyPhrases'])))
"""

def get_response_for_list(list_of_bodys):
	#we should figure out wtf this does
	params = urllib.urlencode({})

	# set up access URL's
	batch = 'westus.api.cognitive.microsoft.com'
	batch_keyphrase_url = '/text/analytics/v2.0/keyPhrases?%s' % params

	header = get_header()
	#list of complied json results
	results = []
	print list_of_bodys
	for block in list_of_bodys:
		request_body = get_request_body(open(block.name).read())
		block.close()
		print sys.getsizeof(request_body)
		#connect and request data for a singular block of a document
		conn = httplib.HTTPSConnection(batch)
		conn.request("POST", batch_keyphrase_url , request_body, header)
		response = conn.getresponse()

		#read and store json response
		result = response.read()
		results.append(result)
		conn.close()

	return results

def get_request_body(block):
	request_body = '{\
			"documents":[\
			{\
			"language": "en", \
			"id" : "1",\
			"text" :' + " '" + str(block) + "' " + '}]}'
	return request_body

def join_responses(responses):
	phrases = {}
	for doc in responses:
		j_doc = json.loads(doc)
		phrase_list = j_doc.get("documents")[0].get("keyPhrases")
		for phrase in phrase_list:
			#print phrase
			if phrase in phrases:
				phrases[phrase] +=1
			else:
				phrases[phrase] = 1
	return phrases

def get_key_words_json_for_doc(filename):
	#try:
		#get list of blocks
		sub_docs = get_list_of_blocks(filename)
		#get responses for these docs
		responses = get_response_for_list(sub_docs)

		#join responses and return top relevant query's
		responses = join_responses(responses)
		for doc in sub_docs:
			os.remove(doc.name)
		return responses
		"""finally:
		if(sub_docs != None):
			for doc in sub_docs:
				os.remove(doc.name)"""

def get_top_n_words(doc, n):
	dochash = hashlib.sha224(doc).hexdigest()
	if dochash in memoized:
		return memoized[dochash]
	else:
		filename = "temp.txt"
		with open(filename, 'w') as file:
			file.write(doc)
			key_words = get_key_words_json_for_doc(filename)
		words = []
		for k, v in key_words.items():
			words.append((k,v))

		words = sorted(words, key=lambda x: x[1])

		memoized[dochash] = words[-n:]
		return words[-n:]

print get_top_n_words('06_4.txt', 5)
