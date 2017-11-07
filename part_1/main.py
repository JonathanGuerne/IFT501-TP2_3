documents = {}
words = {}

results = []


def docs_containing_word(word):
    num_doc = 0
    for document in documents.items():
        if word in document:
            num_doc += 1

    return num_doc


for i in range(1, 4):
    with open('../docwords' + str(i) + '.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            line_array = line.split(" ")
            if line_array[0] not in documents.keys():
                documents[line_array[0]] = []
            documents[line_array[0]].append(line_array[1])
            if line_array[1] not in words.keys():
                words[line_array[1]] = [0,0]
            words[line_array[1]][0] += int(line_array[2][:-1])
            words[line_array[1]][1] += 1


print(len(documents))

print("reading done\n")


i = 0
for word, freq in words.items():
    results.append([word, (freq[0] * (len(documents)) / freq[1])])
    i += 1
    if i % 100 == 0:
        print(str(i / len(words)) + "% \n")

results.sort(key=lambda x: x[1])
results.reverse()

print("results found\nstart writing\n")

words_reduced = []

with open('../results.txt','w',encoding='utf-8') as fou:
    for i in range(20):
        words_reduced.append(results[i][0])
        fou.write(str(results[i][0])+"\n")

with open('../docwordsreduced.txt', 'w', encoding='utf-8') as fou:
    for i in range(1, 4):
        with open('../docwords' + str(i) + '.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                if line.split(' ')[1] in words_reduced:
                    fou.write(line)
