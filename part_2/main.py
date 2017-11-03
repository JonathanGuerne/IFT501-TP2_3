words = []
transactions = {}
clusters = []

with open('../results.txt', 'r', encoding='utf-8') as fin:
    for line in fin:
        words.append(line[:-1])

for i in range(1, 4):
    with open('../docwords' + str(i) + '.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            docword_line = line.split(" ")
            if docword_line[1] in words:
                if docword_line[0] not in transactions.keys():
                    transactions[docword_line[0]] = []
                transactions[docword_line[0]].append(docword_line[1])

print(len(transactions))

for transaction in transactions :
    # assign transaction to a cluster (new or existing) to optimise a criterion function
    pass

move = True
while move:
    for transaction in transactions :
        # assign transaction to a cluster (new or existing) to optimise a criterion function
        pass
        # check if the cluster found is different from the old one
        # if so change the transactions cluster and set move to true



def cf_clusters(clusters):
    somme = 0
    for cluster in clusters :
        somme += (len(cluster)/len(transactions))*cf_cluster(cluster)
    return somme

def cf_cluster(cluster):
    somme = 0
    for transaction in cluster:
        somme += f(transaction,cluster)
    return (1/len(cluster))*somme

def f(transaction, cluster):
    pass