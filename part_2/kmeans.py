import random

words = []
documents = {}
k = 25000 # K = number of documents / 2
clusters = []

with open('../results.txt', 'r', encoding='utf-8') as fin:
    for line in fin:
        words.append(line[:-1])

for i in range(1, 4):
    with open('../docwords' + str(i) + '.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            docword_line = line.split(" ")
            if docword_line[1] in words:
                if docword_line[0] not in documents.keys():
                    documents[docword_line[0]] = []
                documents[docword_line[0]].append(docword_line[1])

random.seed()

for i in range(k):
    pass
    # Random initialisation of clusters


for document in documents:
    pass
    # assign document to the closer cluster

# recalculate new center for the clusters...