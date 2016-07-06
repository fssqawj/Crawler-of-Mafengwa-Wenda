# coding: utf8
import os
from tqdm import tqdm
import sys
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')


def removepunc(strs):
    # return re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。,？、~@#￥%……&*（）]+".decode('utf8'), " ".decode('utf8'), str)
    strs = strs.replace('。', ' ')
    strs = strs.replace(',', ' ')
    strs = strs.replace('，', ' ')
    strs = strs.replace('＂', ' ')
    strs = strs.replace('【', ' ')
    strs = strs.replace('】', ' ')
    strs = strs.replace('（', ' ')
    strs = strs.replace('）', ' ')
    strs = strs.replace('、', ' ')
    strs = strs.replace('…', ' ')
    strs = strs.replace('～', ' ')
    strs = strs.replace('❤', ' ')
    strs = strs.replace('！', ' ')
    strs = strs.replace('？', ' ')
    strs = strs.replace('.', ' ')
    strs = strs.replace('：', ' ')
    strs = strs.replace('；', ' ')
    strs = strs.replace('“', ' ')
    strs = strs.replace('”', ' ')
    strs = strs.replace('￥', ' ')
    strs = strs.replace('-', ' ')
    strs = strs.replace('?', ' ')
    strs = strs.replace('(', ' ')
    strs = strs.replace(')', ' ')
    strs = strs.replace('/', ' ')
    return strs


if __name__ == '__main__':
    # fout = open('traindata.txt', 'w')
    for filename in tqdm(os.listdir('./detail')):
        # for line in open('./detail/' + filename).readlines():
            # if 'TITLE' in line or 'DESC' in line or '_CONTENT' in line:
            #     line = ' '.join(line.split(':')[1:])
            #     fout.write(' '.join(jieba.cut(removepunc(line))))
        if u'日本' in filename:
            fout = open('./japan/' + filename, 'w')
            for line in open('./detail/' + filename).readlines():
                fout.write(line)
