import math
import random
import numpy

#############
#  Classes  #
#############

class Vector:

    def __init__(self):
        self.dimensions = []
        self.dist = math.inf
        self.cluster = None

    def add_dimension(self, dimension):
        self.dimensions.append(dimension)

    def update_dimension(self, index, dimension):
        self.dimensions[index] = dimension

###############
#  Functions  #
###############

def load_results():
    """load results.txt to an array."""
    results = []
    with open('../results.txt', 'r', encoding='utf-8') as fin:
        for word in fin:
            results.append(word)

    return results


def load_docwordsreduced():
    """load docwordsreduces.txt to an array."""
    docwords = []
    with open('../docwordsreduced.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            docwords.append(line[:-1])

    return docwords


def init_vectors(number_of_documents, vector_size):
    """initialize a vector (D=5000) for each documents filled with 0."""
    vectors = []
    for j in range(number_of_documents):
        vectors.append(Vector())
        for i in range(vector_size):
            vectors[j].add_dimension(0)

    return vectors


def find_word_index(word):
    """find the corresponding index to the given word."""
    index = 0
    for line in results:
        if word == int(line):
            return index
        index += 1


def update_vectors(vectors):
    """update the vector of each documents according to the frequency of each word."""
    for line in docwords:
        array_line = line.split(" ")
        index = find_word_index(int(array_line[1]))
        dimension = (int((array_line[2])))
        vectors[(int(array_line[0]) - 1)].update_dimension(index, dimension)


def cosine_similarity(v1, v2):
    """compute the cosine similarity between two vectors."""
    sum_dot = 0
    sum_norm = 0

    for i in range(len(v1)):
        sum_dot += v1[i] * v2[i]
        sum_norm += v1[i] * v1[i]

    if sum_norm != 0:
        return math.acos(sum_dot / math.sqrt(sum_norm))
    else:
        return math.inf


def update_clusters_centers(clusters):
    print("Update clusters centers")
    new_clusters = []

    for cluster in clusters:
        new_cluster = []
        for i in range(number_of_documents):
            new_cluster.append(0)

        number_of_vector = 0
        for vector in vectors:
            if vector.cluster == cluster:  # get throw each vector and check if it belongs to the cluster
                number_of_vector += 1

                index = 0
                for dimension in vector.dimensions:  # if so, add the vector in the mean calculation
                    new_cluster[index] += dimension
                    index += 1

            if number_of_vector != 0:
                for i in range(len(cluster)): # divide the sum by the number of vector in order to get the mean value
                    new_cluster[i] = new_cluster[i] / number_of_vector

        new_clusters.append(new_cluster)

    for i in range(len(clusters)):
        # print(cosine_similarity(clusters[i], new_clusters[i]) - 0.04)
        if cosine_similarity(clusters[i], new_clusters[i]) < 0.04:
            return True

    return False


def k_means(k, vectors):
    clusters = []

    for i in range(k):
        # init cluster with a random vector
        index = random.randrange(0,len(vectors))
        clusters.append(vectors[index].dimensions)

    stable = False
    while not stable:
        for vector in vectors:
            for cluster in clusters:
                dist = cosine_similarity(vector.dimensions, cluster)
                print("dist: " + str(dist))

                if dist < vector.dist:
                    vector.cluster = cluster

        stable = update_clusters_centers(clusters)

##########
#  Main  #
##########

print("Load files")
results = load_results()
docwords = load_docwordsreduced()

print("Init tools")
number_of_documents = int(docwords[-1].split(" ")[0])
vector_size = len(results)

print("Init vectors")
vectors = init_vectors(number_of_documents, vector_size)
update_vectors(vectors)

print("Start K-Means")
random.seed()
k_means(8, vectors)