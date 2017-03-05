import string
import nltk as nltk
from nltk.data import load
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re

"""
	doc          :    the document to be tokenized by sentance
	languange    :    the language the document is in
	returns      :    a list of sentences
"""
def tokenize_text(doc, language = 'english'):
	#tokenizer = load('tokenizers/punkt/{0}.pickle'.format(language))
	#s = re.compile('[.!?]')
	sen = re.compile("[!?.]").split(doc)
	#sen = doc.split('.')
	return sen

"""
	sentances    :    a list of sentences as returned by the tokenizer 
	returns      :    a list of sentences with stopwords and punctuation removed
"""
def remove_stopwords_and_clean(sentances):
	cleaned_sentances = []
	for sentance in sentances:
		stop = set(stopwords.words('english'))
		cleaned_sentances.append([x for x in sentance.lower().split() if x not in stop])
	return cleaned_sentances

"""
	tokenized_list_of_lists    :    a list of sentences with stopwords and punctuation removed 
	returns                    :    a list of the given sentences with each word stemmed
"""
def stem(tokenized_list):
	stemmer = PorterStemmer()
	stemmed = []
	for word_list in tokenized_list:
		w_l = []
		for word in word_list:
			word = word.translate(None, string.punctuation)
			w_l.append(str(stemmer.stem(str(word))))
		stemmed.append(w_l)
	return stemmed

"""
	doc          :    the string to be tokenized stemmed and cleaned
	languange    :    the language the document is in
	returns      :    a list of tokenized, stemmed, and cleaned sentances
"""
def clean_document_and_return_sentances(doc, language='english'):
	sentances = tokenize_text(doc, language)
	return stem(remove_stopwords_and_clean(sentances))

if __name__ == '__main__':
	sens = "text mining is an important aspect of 410? As is text retrival. This sentence is unrelated."
	#print sens
	print tokenize_text(sens)
	print clean_document_and_return_sentances(sens)
