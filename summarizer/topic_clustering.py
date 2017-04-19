import Orange
import orangecontrib.text
from orangecontrib.text import preprocess
from topics import lsi, topics
import gensim
from Orange import data, distance
from Orange.clustering import hierarchical
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import scipy

def process_file(path, num_topics):
	processed_corpus = pre_process(path)

	topic_table = build_topic_model(processed_corpus)
	#print(topic_table[1::])
	linkage = build_linkage_matrix(topic_table)
	hierarch_tree = build_hierarchical_tree(linkage)
	visualize_tree(linkage)
	

def pre_process(path):
	corpus = orangecontrib.text.Corpus.from_file(path)

	p = preprocess.Preprocessor(transformers=[preprocess.LowercaseTransformer(), 
												preprocess.UrlRemover(), 
												preprocess.HtmlTransformer()],
								tokenizer = preprocess.RegexpTokenizer('\w+'),
								normalizer = preprocess.PorterStemmer(),
								filters=[preprocess.StopwordsFilter('english'),
											preprocess.RegexpFilter('\.|,|:|;|!|\?|\(|\)|\||\+|\'|\"|‘|’|“|”|\'|\’|…|\-|–|—|\$|&|\*|>|<')]
											)
	return p(corpus)


def build_topic_model(corpus):
	#parameters = {'num_topics':19, 'Number of topics': 2}
	#model = lsi.LsiWrapper(**{par: parameters[par] for par in parameters})
	model = lsi.LsiWrapper()
	#print(type(model))
	model.reset_model(corpus)
	model.fit(corpus)
	return model.transform(corpus.copy(), num_topics = 1000)

def build_linkage_matrix(topic_table):
	#print(topic_table.domain)
	x = data.Table(topic_table)
	print(x.X)
	dist_matrix = distance.Euclidean(x.X)
	#d = Orange.misc.distmatrix.__new__(dist_matrix)
	print (dist_matrix)
	#linkage = hierarchical.dist_matrix_linkage(dist_matrix,linkage = hierarchical.AVERAGE
	linkage = scipy.cluster.hierarchy.linkage(dist_matrix, method=hierarchical.AVERAGE)
	print((linkage))
	return linkage

def build_hierarchical_tree(X):
	print(type(X))
	#print(X.astype(np.float32))
	return hierarchical.tree_from_linkage(X.astype(np.float32))

def visualize_tree(tree_from_linkage):
	#plt.figure(figsize=(25, 10))
	plt.title('Hierarchical Clustering Dendrogram')
	plt.xlabel('sample index')
	plt.ylabel('distance')
	dendrogram(
    	tree_from_linkage,
    	leaf_rotation=90.,  # rotates the x axis labels
    	leaf_font_size=8.,  # font size for the x axis labels
	)
	plt.show()

if __name__ == '__main__':
	process_file("doc/doc.tab", 3)