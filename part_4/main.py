def init_dic_titles():
    dic_titles = {}
    for i in range(1, 4):
        with open('../doctitles' + str(i) + '.txt', 'r') as fin:
            try:
                for line in fin:
                    line_array = line.split("\t")

                    if len(line_array) > 1:
                        dic_titles[int(line_array[0])] = line_array[1]
            except UnicodeDecodeError:
                pass

    return dic_titles


def print_result_readable(dic_titles):
    with open('./output-clusters.txt', 'r', encoding='utf-8') as fin:
        with open('./output-clusters-readable.txt', 'w', encoding='utf8') as fou:
                for line in fin:
                    try:
                        if line.find("-") != -1:
                            fou.write(line)
                        else:
                            fou.write(dic_titles[int(line)])
                    except ValueError:
                        pass



###MAIN###
dic_titles = init_dic_titles()
print_result_readable(dic_titles)
