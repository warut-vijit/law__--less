import math
# where input is string
def calculate_unigrams(input):
    sum = 0
    counts = {}
    lines = input.split(".")
    for line in lines: # calculate unigram probabilities
        for word in line.split(" "):
            sum += 1
            counts[word.lower()] = 1 if word.lower() not in counts else counts[word.lower()]+1
    sum += len(counts.keys()) # laplacian smoothing
    for key in counts.keys():
        counts[key] = math.log(float(counts[key]+1)/sum)
    unk = math.log(float(1)/sum)
    heap = []
    for line in lines:
        product = 1 # product of probabilities
        split_line = line.split(" ")
        for word in split_line: # generate probability of sentence
            product += unk if word.lower() not in counts else counts[word.lower()]
        if len(split_line) > 4:
            heap.append( (line,product/len(line.split(" "))) )
    sorted_array = sorted( [ x for x in heap if any( [y.isalpha() for y in x[0]] ) ] , key=lambda line: line[1], reverse=True)
    return [x[0] for x in sorted_array[:5]]

# returns array of strings