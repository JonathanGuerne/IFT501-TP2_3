import math
import random
import numpy
import _thread


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


class Cluster:
    def __init__(self):
        self.dimensions = []
        self.dimensions_weight = []

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.dimensions_weight = []

    def add_dimension(self, dimension):
        self.dimensions.append(dimension)

    def update_dimension(self, index, dimension):
        self.dimensions[index] = dimension

    def add_dimension_weight(self, weight):
        self.dimensions_weight.append(weight)

    def update_dimension_weight(self, index, weight):
        self.dimensions_weight[index] = weight


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


def calculate_number_of_documents():
    set = {}

    for line in docwords:
        doc = line.split(" ")[0]
        set[doc] = None

    return len(set)


def init_vectors(vector_size):
    """initialize a vector (D=vector_size) for each documents filled with 0."""
    vectors = {}
    for j in range(len(docwords)):
        doc_id = docwords[j].split(" ")[0]
        vectors[doc_id] = Vector()
        for i in range(vector_size):
            vectors[doc_id].add_dimension(0)
            # vectors[doc_id].add_dimension_weight(0)

    return vectors


def find_word_index(word):
    """find the corresponding index to the given word."""
    index = 0
    for line in results:
        if word == int(line):
            return index
        index += 1

    return EOFError


def update_vectors(vectors):
    """update the vector of each documents according to the frequency of each word."""
    for line in docwords:
        array_line = line.split(" ")
        index = find_word_index(int(array_line[1]))
        dimension = (int((array_line[2])))
        vectors[array_line[0]].update_dimension(index, dimension)


# def init_vectors_weight(vectors, nb_clusters, nb_word_use):
#     """set dimension weight of every vector to the initial value"""
#     for line in docwords:
#         array_line = line.split(" ")
#         index = find_word_index(int(array_line[1]))
#         vectors[array_line[0]].update_dimension_weight(index, nb_clusters * nb_word_use / len(vectors) * nb_word_use)

def euclidean_distance_no_weight(v1, v2):
    sum = 0

    for i in range(len(v1)):
        sum += math.pow((v1[i] - v2[i]), 2)

    return math.sqrt(sum)


def euclidean_distance(v1, v2_weight, v2):
    sum = 0

    for i in range(len(v1)):
        sum += v2_weight[i] * math.pow((v1[i] - v2[i]), 2)

    return math.sqrt(sum)


def update_clusters_centers(clusters):
    print("Update clusters centers")
    new_clusters = []

    for cluster in clusters:
        new_cluster = Cluster()
        for i in range(number_of_documents):  # create new cluster filled with zeroes
            new_cluster.append_dimension(0)

        number_of_vector = 0
        for vector in vectors.values():
            if vector.cluster == cluster:  # get throw each vector and check if it belongs to the cluster
                number_of_vector += 1

                index = 0
                for dimension in vector.dimensions:  # if so, add the vector in the mean calculation
                    new_cluster.update_dimension(index, new_clusters.dimensions[index] + dimension)
                    index += 1

        if number_of_vector != 0:
            for i in range(
                    len(cluster.dimensions)):  # divide the sum by the number of vector in order to get the mean value
                new_cluster.update_dimension(i, new_clusters.dimensions[i] / number_of_vector)
                # new_cluster[i] = new_cluster[i] / number_of_vector

        new_clusters.append(new_cluster)

    is_stable = True
    for i in range(len(clusters)):
        distance = euclidean_distance(clusters[i].dimensions, new_clusters[i].dimensions_weight,
                                      new_clusters[i].dimensions)
        print(distance)
        if distance > numpy.finfo(float).eps:
            is_stable = False

    return new_clusters, is_stable


def print_vector(vector):
    print("------------- Vector ------------")
    for val in vector.dimensions:
        print(val)


def update_clusters_weight(clusters):
    """function use to update the weight of each dimension of each cluster"""

    print("Update clusters weight")
    for cluster in clusters:

        new_weights = []
        sum_wieight_sqr = 0

        for i in range(len(cluster.dimensions)):
            old_weight = cluster.dimensions_weight[i]

            # todo found variance of cluster dim j
            variance = 0.5

            weight = (old_weight / (1 + variance))
            sum_wieight_sqr += pow(weight, 2)
            new_weights.append(weight)

        for i in range(len(cluster.dimensions)):
            cluster.update_dimension_weight(i, new_weights[i] * (len(cluster.dimensions)) / math.sqrt(sum_wieight_sqr))


def get_distance_matrix(vectors):
    distance_matrix = []
    for i in range(len(vectors)):
        distance_matrix[i] = []
        for j in range(len(vectors)):
            if i != j:
                distance_matrix[i][j] = euclidean_distance(vectors[i].dimensions, vectors[j].dimensions)
            else :
                distance_matrix[i][j] = -1


    return distance_matrix


def init_cluster_list(vectors):
    cluster_list = []

    for i in range(len(vectors)):
        cluster_list[0].append(vectors[i])

    return cluster_list


def search_nearest(distance_matrix, vectors, cluster_list):

    min_val = distance_matrix[0][0]
    min_i = 0
    min_j = 0


    for i in range(len(distance_matrix)):
        for j in range(len(distance_matrix[i])):
            if distance_matrix[i][j] != -1 and distance_matrix[i][j] < min_val:
                min_val = distance_matrix[i][j]
                min_i = i
                min_j = j

    new_cluster = []
    new_cluster.append(vectors[min_i])
    new_cluster.append(vectors[min_j])

    cluster_list.append(new_cluster)


    new_vectors = []

    for i in range(len(vectors)):
        if i != min_i and i != min_j :
            new_vectors.append(vectors[i])

    merge_vector = Vector()

    for i in range(len(vectors[i].dimensions)):
        val = vectors[min_i].dimensions[i]+vectors[min_j].dimensions[i]
        val = val / 2.
        merge_vector.add_dimension(val)

    new_vectors.append(merge_vector)

    vectors = new_vectors

    distance_matrix = get_distance_matrix(vectors)





def k_means(k, vectors):
    clusters = []

    for i in range(k):
        # init cluster with a random vector
        list_keys = list(vectors.keys())
        key = str(random.choice(list_keys))
        cluster = Cluster(vectors[key].dimensions)
        for i in range(len(cluster.dimensions)):
            cluster.add_dimension_weight(1)
        clusters.append(cluster)

    stable = False
    while not stable:
        print("K-Means")
        for vector in vectors.values():
            for cluster in clusters:
                dist = euclidean_distance(vector.dimensions, cluster.dimensions_weight, cluster.dimensions)

                if dist < vector.dist:
                    vector.cluster = cluster

        update_clusters_weight(clusters)
        clusters, stable = update_clusters_centers(clusters)

    with open('output-clusters.txt', 'w', encoding='utf-8') as fou:
        for out_cluster in clusters:
            empty = True
            for key, vector in vectors.items():
                if vector.cluster == out_cluster:
                    fou.write(key + "\n")
                    empty = False

            if not empty:
                fou.write("\n" + "-" * 50 + "\n")


##########
#  Main  #
##########

print("Load files")
results = load_results()
docwords = load_docwordsreduced()

print("Init tools")
number_of_documents = calculate_number_of_documents()
vector_size = len(results)

print("Init vectors")
vectors = init_vectors(vector_size)
update_vectors(vectors)

distance_matrix = get_distance_matrix(vectors)

cluster_list = init_cluster_list(vectors)

search_nearest(distance_matrix,vectors,cluster_list)


#print("Start K-Means")
#random.seed()
#k_means(nb_clusters, vectors)
