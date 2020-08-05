# coding=utf-8
import requests
import traceback
from bs4 import BeautifulSoup
import threading
import random
import time
import os
from math import ceil
from gen.gen_ncx import ncx
from gen.gen_opf import opf
from gen.gen_top_html import top_html
from gen.gen_content import content_html
import re


def get_content(url):
    while True:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
            r = requests.request('get', url, headers=headers)
            # time.sleep(random.randint(3, 4))
            r.encoding = 'utf-8'
            if r.status_code != 200:
                print('***' + url)
                continue
            return BeautifulSoup(r.text, 'lxml')
        except BaseException:
            traceback.print_exc()
            continue


class Down(threading.Thread):
    def __init__(self, top_soup_list,chap_list):
        threading.Thread.__init__(self)
        self.top_soup_list = top_soup_list
        self.chap_list = chap_list

    def run(self):
        for chap_url_soup in self.top_soup_list:
            if chap_url_soup['href'].startswith('http'):
                continue
            chap_name = chap_url_soup.text.strip()
            chap_name = re.sub('\s*【.*', '', chap_name)
            chap_name = re.sub('\s+', ' ', chap_name)
            content_soup = get_content(rootUrl + chap_url_soup['href'])
            chap = dict()
            chap['chap_name'] = chap_name
            chap['idx'] = chap_url_soup.idx
            print(chap_name)
            chap_content = []
            content_list = content_soup.select('[id="content"] p')
            for chap_soup in content_list:
                chap_content.append(chap_soup.text)
            chap['content'] = chap_content[0:-1]
            chap['url'] = chap_url_soup['href']
            self.chap_list.append(chap)

def get_new_soup(top_soup_list):
    i = 0
    for t in top_soup_list:
        t.idx = i
        i += 1
    new_top_soup_list = list()
    total = len(top_soup_list)
    step = int(ceil(float(total) / 10.0))
    for i in range(0, total, step):
        char_list = top_soup_list[i:i + step]
        down = Down(char_list, new_top_soup_list)
        down.start()
    lth = 0
    while True:
        time.sleep(20)
        if len(new_top_soup_list) - lth == 0:
            new_top_soup_list.sort(key=lambda tag:tag['idx'])
            return new_top_soup_list
        lth = len(new_top_soup_list)


if __name__ == '__main__':
    noveurl = 'https://www.d586.com/4414/'
    rootUrl = 'https://www.d586.com'
    top_soup = get_content(noveurl)
    novel_name = top_soup.select('[property="og:novel:book_name"]')[0]['content']
    en_name = 'qugekongjie'
    root_path = 'D:\\jin\\' + novel_name
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    top_soup_list = top_soup.select('[id="list"] a')[13:]
    dc_info = dict()
    dc_info['Title'] = novel_name
    dc_info['Language'] = 'zh-CN'
    dc_info['Creator'] = top_soup.select('[property="og:novel:author"]')[0]['content']
    dc_info['Copyrights'] = 'zrc'
    dc_info['Publisher'] = 'zrc'
    chap_list = get_new_soup(top_soup_list)
    ncx_list = []
    top_info = []
    item_info = list()
    item_info.append({'id': en_name, 'href': en_name + '.html'})
    ncx_map = {'text': novel_name, 'src': en_name + '.html', 'child': []}
    top = {'book_title': novel_name, 'book_url': en_name + '.html', 'child_tops': []}
    i = 1
    for chap_url_soup in chap_list:
        chap = dict()
        chap_name = chap_url_soup['chap_name']
        chap['chap_name'] = chap_name
        child_top = {'chap_title': chap_name, 'chap_url': en_name + '.html#%s' % i}
        top['child_tops'].append(child_top)
        ncx_map['child'].append({'text': chap_name, 'src': en_name + '.html#%s' % i})
        i += 1
    ncx_list.append(ncx_map)
    content_html(root_path, en_name, chap_list)
    top_info.append(top)
    ncx(root_path, novel_name, ncx_list)
    opf(root_path, dc_info, item_info)
    top_html(root_path, novel_name, top_info, True)




