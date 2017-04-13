import numpy as np
import scipy.linalg as spl

'''
len_adj_matrix: The size of the adj matrix
returns       : A nunpy array filled with 1/(size of adj matrix)
'''
def build_probability_matrix(len_adj_matrix):
    p_matrix = np.zeros(( len_adj_matrix , len_adj_matrix ))
    probability = 1 / float(len_adj_matrix)
    p_matrix.fill(probability)
    return p_matrix

'''
s_array: A list of sentences where each sentence is a list of terms
vecs   : A list of eigen vectors that contain textrank scores
returns: An array where each index of the array has a score and that index is
        the same as the order in which the sentence was passed in
'''
def get_sentence_scores(s_array, vecs):
    scores = []
    for s in range( len( s_array ) ):
        print s
        print abs(vecs[s][0])
        scores.append(abs(vecs[s][0]))
    return scores

'''
adj_matrix    : A matrix where each sentence is adjacent by some weight
d             : A dampening factor
epsilon       : threshold of convergance
maxIterations : max iterations before convergance is assumed
returns       : A list of eigen vectors that contain textrank scores, the indicies
            of these values are the same as the s_array
'''
def textrank(adj_matrix, d, epsilon=0.00001, maxIterations=1000):

    #creating the random jumping matrix -- filled with 1/N
    prob_matrix = build_probability_matrix(len(adj_matrix))

    #creating the textrank matrix using dampening
    tr_matrix = d * adj_matrix + (1 - d) * prob_matrix

    #old_state = np.copy(tr_matrix)

    power_matrix = np.empty_like(tr_matrix)
    power_matrix.fill(.25)

    for iteration in range(maxIterations):
        old_state = np.copy(tr_matrix)
        tr_matrix = tr_matrix.dot(power_matrix)
        delta = tr_matrix - old_state
        if np.sum(np.abs(tr_matrix - old_state)) < epsilon:
            break

    vectors = []
    for vec in tr_matrix.T:
        vectors.append(vec)
    return vectors
    #using scipy left eigenvector to grab scores
    #values, vectors = spl.eig(tr_matrix, left=True, right=False)

'''
s_array: A list of sentences where each sentence is a list of terms
scores : sentence scores
n      : Number of sentences to return
returns: n best sentences
'''
def get_n_best_sentences(s_array, scores, n):
    #just in case
    if n > len(s_array):
        n = len(s_array)
    #make them into score, sentence tuples
    score_sentence = [(scores[i] , s_array[i]) for i in range(len(s_array))]
    #sort these tuples
    sorted_score_sentence_index = sorted(range(len(score_sentence)), key=lambda x: score_sentence[x])[-n:]
    sorted_score_sentence_index.sort()    #grab the n best
    best_n = [score_sentence[sorted_score_sentence_index[i]][1] for i in range(n)]
    return best_n
###########################This is effectively the main#########################
'''
adj_matrix: A matrix where each sentence is adjacent by some weight
d         : A dampening factor
s_array   : A list of sentences where each sentence is a list of terms
returns   : An array where each index of the array has a score and that index is
the same as the order in which the sentence was passed in
'''
def run_textrank_and_return_n_sentences(adj_matrix, s_array, d, n):
    eigen_vectors =  textrank(adj_matrix, d)
    scores = get_sentence_scores(s_array, eigen_vectors)
    best_sentences = get_n_best_sentences( s_array, scores, n)
    return best_sentences

###########################Silly Test###########################################
# vec = textrank(test_adj_matrix, .80)
# print vec
# scores = get_sentence_scores(test,vec)
# print scores
# match_score_and_sentence(test,scores)
