# Simple program that demonstrates how to invoke Azure ML Text Analytics API: topic detection.
import httplib
import urllib
import sys
import base64
import json
import time

# Azure portal URL.
base_url = 'https://westus.api.cognitive.microsoft.com/'

# read key from file
account_key = ''

with open('azure_key.txt') as file:
	account_key = file.readline().strip()

headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}

# Path to file with JSON inputs.
file_path = '06_1.txt'
f = open(file_path, 'r')
input_text = f.read()
print input_text

input_texts = '{\
				"documents":[\
				{\
				"language": "en", \
				"id" : "1",\
				"text" :' + " '" + input_text + "' " + '}]}'
print type(input_texts)
num_detect_langs = 1;

params = urllib.urlencode({
})

# Detect key phrases.
batch = 'westus.api.cognitive.microsoft.com'
batch_keyphrase_url = '/text/analytics/v2.0/keyPhrases?%s' % params

#print batch_keyphrase_url

conn = httplib.HTTPSConnection(batch)
conn.request("POST", batch_keyphrase_url , input_texts, headers)
response = conn.getresponse()
#print response
result = response.read()
print result
conn.close()

obj = json.loads(result)
for keyphrase_analysis in obj['documents']:
	print('Key phrases ' + str(keyphrase_analysis['id']) + ': ' + ', '.join(map(str,keyphrase_analysis['keyPhrases'])))

"""
# Detect language.
language_detection_url = base_url + 'text/analytics/v2.0/languages' + ('?numberOfLanguagesToDetect=' + num_detect_langs if num_detect_langs > 1 else '')
req = urllib2.Request(language_detection_url, input_texts, headers)
response = urllib2.urlopen(req)
result = response.read()
obj = json.loads(result)
for language in obj['documents']:
    print('Languages: ' + str(language['id']) + ': ' + ','.join([lang['name'] for lang in language['detectedLanguages']]))

# Detect sentiment.
batch_sentiment_url = base_url + 'text/analytics/v2.0/sentiment'
req = urllib2.Request(batch_sentiment_url, input_texts, headers) 
response = urllib2.urlopen(req)
result = response.read()
obj = json.loads(result)
for sentiment_analysis in obj['documents']:
    print('Sentiment ' + str(sentiment_analysis['id']) + ' score: ' + str(sentiment_analysis['score'])) """
