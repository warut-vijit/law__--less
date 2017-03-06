import string
import nltk as nltk
from nltk.data import load
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def tokenize_text(doc, language = 'english'):
	#PunktSentenceTokenizer.tokenize(doc)
	tokenizer = load('tokenizers/punkt/{0}.pickle'.format(language))
	sen = tokenizer.tokenize(doc)
	return sen

def stem(tokenized_list_of_lists):
	stemmer = PorterStemmer()
	stemmed = []
	for word_list in tokenized_list_of_lists:
		w_l = []
		for word in word_list:
			word = word.translate(None, string.punctuation)
			w_l.append(str(stemmer.stem(str(word))))
		stemmed.append(w_l)
	return stemmed

def remove_stopwords(sentances):
	cleaned_sentances = []
	for sentance in sentances:
		stop = set(stopwords.words('english'))
		cleaned_sentances.append([x for x in sentance.lower().split() if x not in stop])
	return cleaned_sentances

#nltk.download()
sens = tokenize_text("text mining is an important aspect of 410. As is text retrival. This sentence is unrelated.")
print sens
print stem(remove_stopwords(sens))

#stemmer = PorterStemmer()
#print stemmer.stem("running.")