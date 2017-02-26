import math
# where input is string
def calculate_unigrams(input, keywords):
    sum = 0
    counts = {}
    lines = input.split(".")
    for line in lines: # calculate unigram probabilities
        for word in line.split(" "):
            sum += 1
            counts[word.lower()] = 1 if word.lower() not in counts else counts[word.lower()]+1
    sum += len(counts.keys()) # laplacian smoothing
    for key in counts.keys():
        keyword_weight = 1.5 if key in [x[0].lower() for x in keywords] else 1.0
        counts[key] = math.log(float(counts[key]+1)/sum*keyword_weight)
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