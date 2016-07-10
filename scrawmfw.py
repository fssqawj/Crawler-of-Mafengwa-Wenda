# coding: utf8
import os
import codecs
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def fetch(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.text


def getdetaillist(htmlstr):
    detaillist = htmlstr.split(r'href=\"\/wenda\/detail-')[1:]
    detailid = [x[0:x.index('.html')] for x in detaillist]
    return detailid


def getmddid(htmlstr):
    soup = BeautifulSoup(htmlstr)
    mdd = soup.select('a._j_change_list._j_change_mdd')
    fout = codecs.open('mddid.txt', 'w', 'utf-8')
    for item in mdd:
        fout.write(item['href'] + '\t' + item['title'] + '\t' + item.em.get_text() + '\t' + item['data-mddid'] + '\n')


def process(mdd, detailid, htmlstr):
    fout = codecs.open('latast/' + mdd + '_' + detailid + '.txt', 'w', 'utf-8')
    soup = BeautifulSoup(htmlstr)
    if len(soup.select('div.q-title')) == 0:
        return
    title = soup.select('div.q-title')[0].h1.get_text()
    desc = soup.select('div.q-desc')[0].get_text()
    pubtime = soup.select('div.pub-bar')[0].span.get_text()
    tags = ""
    taglist = soup.select('div.q-tags.fl')[0].find_all('a')
    for tag in taglist:
        tags += tag.get_text() + "#"
    fout.write('REGIN:' + mdd + '\n')
    fout.write('ID:' + detailid.strip() + '\n')
    fout.write('TITLE:' + title.strip() + '\n')
    fout.write('DESC:' + desc.strip() + '\n')
    fout.write('TAGS:' + tags + '\n')
    fout.write('PUBTIME:' + pubtime.strip() + '\n')
    retreslist = soup.select('li.answer-item')
    retressize = len(retreslist)
    fout.write('RETRESSIZE:' + str(retressize) + '\n')
    rescnt = 0
    for retres in retreslist:
        content = retres.select('div.answer-content')[0].get_text()
        cntzan = retres.select('a.btn-zan')[0].get_text()
        ptime = retres.select('div.pub-time')[0].get_text()
        fout.write('RETRES_' + str(rescnt) + '_CONTENT:' + content.strip().replace('\n', '') + '\n')
        fout.write('RETRES_' + str(rescnt) + '_CNTZAN:' + cntzan.strip() + '\n')
        fout.write('RETRES_' + str(rescnt) + '_PTIME:' + ptime.strip() + '\n')
        rescnt = rescnt + 1

if __name__ == '__main__':
    ''' getmddid code
    htmlstr = fetch('http://www.mafengwo.cn/wenda/')
    getmddid(htmlstr)
    '''
    ''' getdetaillist code
    urlformat = 'http://www.mafengwo.cn/qa/ajax_pager.php?type=0&mddid={}&tids=0&app_link=&action=question_index&start={}'
    for line in tqdm(open('mddid.txt').readlines()):
        line = line.split('\t')
        fout = codecs.open('mfwdata/' + line[1] + '.txt', 'w', 'utf-8')
        for i in range(0, min(500, int(line[2])), 20):
            htmlstr = fetch(urlformat.format(line[3], i))
            detailid = getdetaillist(htmlstr)
            for item in detailid:
                fout.write(item + '\n')
        fout.close()
    '''
    ''' getwendadata code
    detailfile = os.listdir('./mfwdata')
    for df in detailfile:
        for detailid in open('mfwdata/' + df).readlines():
            detailid = detailid.strip()
            # print 'http://www.mafengwo.cn/wenda/detail-' + detailid + '.html'
            if os.path.exists(r'/home/fssqawj/tourQA/detail/' + df[0:df.index('.')] + '_' + detailid + '.txt'):
                print 'EXIT!'
                continue
            print detailid
            htmlstr = fetch('http://www.mafengwo.cn/wenda/detail-' + detailid + '.html')
            process(df[0:df.index('.')], detailid, htmlstr)
    '''
    '''
    urlformat = 'http://www.mafengwo.cn/qa/ajax_pager.php?type=1&mddid=0&tids=0&app_link=&action=question_index&start={}'
    fout = open('latastdetailid.txt', 'w')
    for i in range(0, 500, 20):
        htmlstr = fetch(urlformat.format(i))
        detailid = getdetaillist(htmlstr)
        for item in detailid:
            fout.write(item + '\n')
    fout.close()
    '''
    for line in open('latastdetailid.txt').readlines():
        line = line.strip()
        htmlstr = fetch('http://www.mafengwo.cn/wenda/detail-' + line + '.html')
        process('latast-7-7', line, htmlstr)
