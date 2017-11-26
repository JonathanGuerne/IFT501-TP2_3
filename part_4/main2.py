import math
import random
import numpy
import statistics


#############
#  Classes  #
#############

class Vector:
    def __init__(self):
        self.components_array = []
        self.distance = math.inf
        self.cluster_id = None

    def add_component(self, component):
        self.components_array.append(component)

    def update_component(self, index, component):
        self.components_array[index] = component


class Cluster:
    def __init__(self, id):
        self.center = []
        self.components_weight_array = []
        self.id = id
        self.vectors_array = []

    def set_center(self, center):
        self.center = center

    def add_component(self, component):
        self.center.append(component)

    def update_component(self, index, component):
        self.center[index] = component

    def add_component_weight(self, weight):
        self.components_weight_array.append(weight)

    def update_component_weight(self, index, weight):
        self.components_weight_array[index] = weight


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
    """initialize a vector (number of results = vector_size) for each documents filled with 0."""
    vectors = {}
    for j in range(len(docwords)):
        doc_id = docwords[j].split(" ")[0]
        vectors[doc_id] = Vector()
        for i in range(vector_size):
            vectors[doc_id].add_component(0)

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
        component = (int((array_line[2])))
        vectors[array_line[0]].update_component(index, component)


def euclidean_distance(v1, v2_weight, v2):
    sum = 0

    for i in range(len(v1)):
        sum += v2_weight[i] * math.pow((v1[i] - v2[i]), 2)

    return math.sqrt(sum)


def update_clusters_centers(clusters):
    print("Update clusters centers")
    new_clusters = []

    for cluster in clusters:
        new_cluster = cluster
        for i in range(vector_size):  # create new cluster filled with zeroes
            new_cluster.update_component(i, 0)

        for vector in cluster.vectors_array:
            index = 0
            for component in vector.components_array:  # if so, add the vector in the mean calculation
                new_cluster.center[index] += component
                index += 1

        number_of_vector = len(cluster.vectors_array)
        if number_of_vector != 0:
            for i in range(len(cluster.center)):  # divide the sum by the number of vector -> mean value
                new_cluster.center[i] = new_cluster.center[i] / number_of_vector

        new_clusters.append(new_cluster)

    is_stable = True
    for i in range(len(clusters)):
        distance = euclidean_distance(clusters[i].center, new_clusters[i].components_weight_array,
                                      new_clusters[i].center)

        if distance > numpy.finfo(float).eps:
            is_stable = False

    return new_clusters, is_stable


def update_vectors_of_cluster(cluster):
    for vector in vectors.values():
        if vector.cluster_id == cluster.id:  # get throw each vector and check if it belongs to the cluster
            cluster.vectors_array.append(vector)


def update_clusters_weight(clusters):
    """function use to update the weight of each vector of each cluster"""

    print("Update clusters weight")
    for cluster in clusters:

        new_weights = []
        sum_weights_sqr = 0

        update_vectors_of_cluster(cluster)

        number_of_vectors = len(cluster.vectors_array)

        if number_of_vectors > 0:

            for i in range(len(cluster.center)):
                old_weight = cluster.components_weight_array[i]

                variance_values = []
                for j in range(number_of_vectors):
                    variance_values.append(cluster.vectors_array[j].components_array[i])

                variance = 0
                if len(variance_values) > 1:
                    variance = statistics.variance(variance_values)

                weight = (old_weight / (1 + variance))
                new_weights.append(weight)
                sum_weights_sqr += pow(weight, 2)

            for i in range(len(cluster.center)):
                cluster.update_component_weight(i, new_weights[i] * (len(cluster.center)) / math.sqrt(sum_weights_sqr))
                print(cluster.components_weight_array)


def k_means(k, vectors):
    clusters = []

    for i in range(k):
        # init cluster with a random vector
        list_keys = list(vectors.keys())
        key = str(random.choice(list_keys))
        cluster = Cluster(i)
        cluster.set_center(vectors[key].components_array)
        for i in range(len(cluster.center)):
            cluster.add_component_weight(1)
        clusters.append(cluster)

    stable = False
    while not stable:
        print("K-Means")
        for vector in vectors.values():  # Find the closest cluster of the vector
            for cluster in clusters:
                distance = euclidean_distance(vector.components_array, cluster.components_weight_array, cluster.center)

                if distance < vector.distance:
                    vector.cluster_id = cluster.id
                    vector.distance = distance

        update_clusters_weight(clusters)
        clusters, stable = update_clusters_centers(clusters)

    for cluster in clusters:
        weights = cluster.components_weight_array
        weights.sort()
        weights.reverse()

        for weight in weights:
            print(str(weight))

        print("\n" + "-" * 50 + "\n")


##########
#  Main  #
##########

if __name__ == '__main__':
    nb_clusters = 3

    print("Load files")
    results = load_results()
    docwords = load_docwordsreduced()

    print("Init tools")
    number_of_documents = calculate_number_of_documents()
    vector_size = len(results)

    print("Init vectors")
    vectors = init_vectors(vector_size)
    update_vectors(vectors)

    print("Start K-Means")
    random.seed()
    k_means(nb_clusters, vectors)
