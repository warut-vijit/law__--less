import string
import nltk as nltk
from nltk.data import load
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re

"""
	text         :    the document to be tokenized by sentance
	languange    :    the language the document is in
	returns      :    a list of sentences
"""
def tokenize_text(text, language = 'english'):
	#regex patterns for specfic edge cases
	caps = "([A-Z])"
	prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
	suffixes = "(Inc|Ltd|Jr|Sr|Co)"
	starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
	acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
	websites = "[.](com|net|org|io|gov)"

	text = " " + text + "  "
	text = text.replace("\n"," ")
	text = re.sub(prefixes,"\\1<prd>",text)
	text = re.sub(websites,"<prd>\\1",text)
	if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
	text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
	text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
	text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
	text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
	text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
	text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
	text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
	if "\"" in text: text = text.replace(".\"","\".")
	if "!" in text: text = text.replace("!\"","\"!")
	if "?" in text: text = text.replace("?\"","\"?")
	text = text.replace(".",".<stop>")
	text = text.replace("?","?<stop>")
	text = text.replace("!","!<stop>")
	text = text.replace("<prd>",".")
	sentences = text.split("<stop>")
	sentences = sentences[:-1]
	sentences = [s.strip() for s in sentences]
	return sentences

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
	#nltk.download()
	sens = "text mining is an important aspect of 410. As is text retrival. This sentence is unrelated."
	print sens
	print tokenize_text(sens)
