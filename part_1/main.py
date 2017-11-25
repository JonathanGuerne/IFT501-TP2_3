import math

documents = {}  # Document : [list of words]
words = {}

results = []  # frequents words

for i in range(1, 4):
    with open('../docwords' + str(i) + '.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            line_array = line.split(" ")
            if line_array[0] not in documents.keys():  # Check if the document already exists
                documents[line_array[0]] = []
            documents[line_array[0]].append(line_array[1])  # Add the word to the document
            if line_array[1] not in words.keys():
                words[line_array[1]] = [0, 0]
            words[line_array[1]][0] += int(line_array[2][:-1])
            words[line_array[1]][1] += 1

print(len(documents))

print("reading done\n")

for word, freq in words.items():
    results.append([word, (freq[0] * (len(documents)) / freq[1])])

results.sort(key=lambda x: x[1])
results.reverse()

print("results found\nstart writing\n")

words_reduced = []

with open('../results.txt', 'w', encoding='utf-8') as fou:
    for i in range(100):
        words_reduced.append(results[i][0])
        fou.write(str(results[i][0]) + "\n")


with open('../docwordsreduced.txt', 'w', encoding='utf-8') as fou:
    for i in range(1, 4):
        with open('../docwords' + str(i) + '.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                line_array = line.split(' ')
                if line_array[1] in words_reduced:
                    fou.write(line)

print("End")
