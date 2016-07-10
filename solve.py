# coding: utf8
import gensim
import math
from processdata import removepunc
import os
from tqdm import tqdm
import sys
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')


def gettitleandtags(filepath):
    qa = {}
    for line in open(filepath).readlines():
        if 'TITLE' in line:
            qa['title'] = ' '.join(line.split(':')[1:])
        if 'TAGS' in line:
            qa['tags'] = ' '.join(line.split(':')[1:])
    return qa


def getqadata(detaildir):
    qadata = []
    for filename in os.listdir(detaildir):
        qa = gettitleandtags('./detail/' + filename)
        qadata.append(qa)
    return qadata


def tagsim(rettag, usertag):
    ret = rettag.split('#')
    user = usertag.split('#')
    cotag = [tag for tag in ret if tag in user]
    return 1.0 * len(cotag) / (max(len(ret), len(user)) + 1)


def questionsim(retq, userq, model):
    ret = jieba.cut(removepunc(retq))
    user = jieba.cut(removepunc(userq))
    res = 0.0
    for x in ret:
        if x == '' or x == ' ':
            continue
        for y in user:
            if y == '' or y == ' ':
                continue
            if x == y:
                res += 1.0
            else:
                try:
                    sim = model.similarity(x, y)
                    if sim >= 0.6:
                        res += sim
                except:
                    pass
    return res / math.sqrt(len(list(ret)) * len(list(user)) + 1)


def calcpair(retqa, userq, model):
    # print retqa.get('title', '') + '####' + userq.get('title', '')
    score = tagsim(retqa.get('tags', ''), userq.get('tags', '')) * 2 + questionsim(retqa.get('title', ''), userq.get('title', ''), model)
    return score


def calc(qadata, userq, k, model):
    score = [calcpair(retqa, userq, model) for retqa in qadata]
    res = zip(qadata, score)
    res = sorted(res, key=lambda x: x[1], reverse=True)
    fout = open('temres.txt', 'w')
    fout.write('USERQ:' + userq['title'] + '\n')
    fout.write('USERTAG:' + userq['tags'] + '\n')
    for i in range(k):
        fout.write('RES:' + res[i][0]['title'] + '\n')
        fout.write('RES:' + res[i][0]['tags'] + '\n')


if __name__ == '__main__':
    qadata = getqadata('./detail')
    userq = gettitleandtags('./latast/latast-7-7_7032850.txt')
    model = gensim.models.Word2Vec.load_word2vec_format("tourvecmodel.txt", binary=False)
    calc(qadata, userq, 3, model)
