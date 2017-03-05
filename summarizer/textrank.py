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
returns: An array where each index of the array has a score and that index is the same as the order
in which the sentence was passed in
'''
def get_sentence_scores(s_array, vecs):
    scores = []
    for s in range( len( s_array ) ):
        print s
        print abs(vecs[s][0])
        scores.append(abs(vecs[s][0]))
    return scores

'''
adj_matrix  : A matrix where each sentence is adjacent by some weight
d           : A dampening factor
returns     : A list of eigen vectors that contain textrank scores, the indicies
of these values are the same as the s_array
'''
def textrank(adj_matrix, d):

    #creating the random jumping matrix -- filled with 1/N
    prob_matrix = build_probability_matrix(len(adj_matrix))

    #creating the textrank matrix using dampening
    tr_matrix = d * adj_matrix + (1 - d) * prob_matrix

    #using scipy left eigenvector to grab scores
    values, vectors = spl.eig(tr_matrix, left=True, right=False)
    return vectors


###########################Silly Test###########################################
# vec = textrank(test_adj_matrix, .80)
# print vec
# scores = get_sentence_scores(test,vec)
# print scores
# match_score_and_sentence(test,scores)
