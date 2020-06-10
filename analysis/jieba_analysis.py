import jieba
from collections import OrderedDict, Counter


for i in range(13, 14):
    stoplist = [line.strip("\n") for line in open('stop.txt', 'r', encoding="utf8").readlines()]

    txt = open(f"data/bad_review_small_{i}_test.txt", "r").read()
    # jieba.load_userdict("dict.txt")
    words = jieba.cut(txt)

    data = (word for word in words if word not in stoplist)
    dic = Counter(data)
    ls = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    results = OrderedDict(ls)

    file = open(f'data/small_{i}.txt', mode='w')

    for word, count in results.items():
        new_context = word + "   " + str(count) + '\n'
        file.write(new_context)

    file.close()
