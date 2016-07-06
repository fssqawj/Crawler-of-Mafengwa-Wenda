# coding: utf8
import os


if __name__ == '__main__':
    # tag = set()
    for filename in os.listdir('./japan/'):
        for line in open('./japan/' + filename).readlines():
            if 'TAGS:' in line and ('餐厅' in line or '美食' in line or '酒吧' in line):
                # line = line[5:]
                # line = line.split('#')
                # for item in line:
                #     tag.add(item)
                fout = open('./japancarting/' + filename, 'w')
                for line in open('./japan/' + filename).readlines():
                    fout.write(line)
