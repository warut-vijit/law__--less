from summarizer.topic_extractor import *
import logging
import json

def do_things(cleaned_string, query_text):
	#doc = "The fox dog it. foot grazed the sleeping. The fox waking it."
	#test_search(doc)
	sentences = tokenize_text(cleaned_string)
	#print sentences
	stemmed_sentences = clean_document_and_return_sentances(cleaned_string)
	adj_matrix = create_sentence_adj_matrix(sentences)
	adj_matrix = update_graph_with_query(adj_matrix, query_text)
	logging.error("finished running do_things")

	return adj_matrix

if __name__ == '__main__':
	cleaned_string = open("cleaned.txt").read()
	query_text = open("query.txt").read()
	open("cleaned.txt", "w").write(json.dumps(do_things(cleaned_string, query_text).tolist()))
