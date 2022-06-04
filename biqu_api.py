# coding=utf-8
import requests
import traceback
import threading
import random
import time
import os
from math import floor

from gen.gen_ncx import ncx
from gen.gen_opf import opf
from gen.gen_top_html import top_html
from gen.gen_content import content_html
import re
import json

# 搜索 https://souxs.leeyegy.com/search.aspx?key=头狼&siteid=app2
# 目录 https://infosxs.pysmei.com/BookFiles/Html/429/428286/index.html
# 正文 https://infosxs.pysmei.com/BookFiles/Html/429/428286/2405485.html



def get_content(url):
    while True:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
            r = requests.request('get', url, headers=headers)
            r.encoding = 'utf-8-sig'
            if r.status_code != 200:
                print('***' + url)
                continue
            text = r.text
            text = text.replace(',]', ']')
            return json.loads(text)
        except BaseException as e:
            time.sleep(random.randint(3, 4))
            traceback.print_exc()
            continue


class Down(threading.Thread):
    def __init__(self, top_soup_list, chap_list):
        threading.Thread.__init__(self)
        self.top_soup_list = top_soup_list
        self.chap_list = chap_list

    def run(self):
        while True:
            if len(top_soup_list) == 0:
                break
            chap_url_soup = self.top_soup_list.pop(0)
            chap_name = chap_url_soup['name']
            print(chap_name)
            content_soup = get_content(noveurl.replace('index', str(chap_url_soup['id'])))
            chap = dict()
            chap['chap_name'] = chap_name
            chap['idx'] = chap_url_soup['idx']
            content_list = content_soup['data']['content']
            chap_content = re.split('\s{2,}', content_list)
            chap_content = list(filter(lambda x: x!='', chap_content))
            chap['content'] = chap_content
            chap['url'] = f'/{book_id}/{chap_url_soup["id"]}.html'
            self.chap_list.append(chap)


def get_new_soup(top_soup_list):
    i = 0
    for t in top_soup_list:
        t['idx'] = i
        i += 1
    char_list = list()
    for i in range(10):
        down = Down(top_soup_list, char_list)
        down.start()
        # down.run()
    while True:
        if 0 == len(top_soup_list):
            char_list.sort(key=lambda tag: tag['idx'])
            return char_list
        time.sleep(5)


if __name__ == '__main__':
    book_id = 428286
    noveurl = f'https://infosxs.pysmei.com/BookFiles/Html/{floor(book_id / 1000) + 1}/{book_id}/index.html'
    top_soup = get_content(noveurl)
    novel_name = top_soup['data']['name']
    en_name = 'qugekongjie'
    root_path = 'D:\\jin\\' + novel_name
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    top_soup_list = top_soup['data']['list'][0]['list']
    dc_info = dict()
    dc_info['Title'] = novel_name
    dc_info['Language'] = 'zh-CN'
    dc_info['Creator'] = 'zrc'
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
