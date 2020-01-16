# coding=utf-8
import requests
import traceback
from bs4 import BeautifulSoup
import os
from gen_ncx import ncx
from gen_opf import opf
from gen_top_html import top_html
from gen_content import content_html
import re
import time
import random


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


noveurl = 'https://www.d586.com/4607/'
rootUrl = 'https://www.d586.com'
top_info = []
ncx_list = []
item_info = list()
top_soup = get_content(noveurl)
novel_name = top_soup.select('[property="og:novel:book_name"]')[0]['content']
root_path = 'D:\\jin\\' + novel_name
if not os.path.exists(root_path):
    os.mkdir(root_path)
dc_info = dict()
dc_info['Title'] = novel_name
dc_info['Language'] = 'zh-CN'
dc_info['Creator'] = top_soup.select('[property="og:novel:author"]')[0]['content']
dc_info['Copyrights'] = 'zrc'
dc_info['Publisher'] = 'zrc'


en_name = 'qugekongjie'
book_name = novel_name
print(novel_name + '--->' + book_name)
top = {'book_title': book_name, 'book_url': en_name + '.html', 'child_tops': []}
ncx_map = {'text': book_name, 'src': en_name + '.html', 'child': []}

item_info.append({'id': en_name, 'href': en_name + '.html'})
chap_list = []
i = 1
top_soup_list = top_soup.select('[id="list"] a')[13:]
for chap_url_soup in top_soup_list:
    if chap_url_soup['href'].startswith('http'):
        continue
    chap_name = chap_url_soup.text.strip()
    chap_name = re.sub('\s*【.*', '', chap_name)
    chap_name = re.sub('\s+', ' ', chap_name)
    content_soup = get_content(rootUrl + chap_url_soup['href'])
    chap = dict()
    chap['chap_name'] = chap_name
    child_top = {'chap_title': chap_name, 'chap_url': en_name + '.html#%s' % i}
    top['child_tops'].append(child_top)
    ncx_map['child'].append({'text': chap_name, 'src': en_name + '.html#%s' % i})
    print(chap_name)
    chap_content = []
    content_list = content_soup.select('[id="content"] p')
    for chap_soup in content_list:
        chap_content.append(chap_soup.text)
    chap['content'] = chap_content[0:-1]
    chap_list.append(chap)
    i += 1
ncx_list.append(ncx_map)
content_html(root_path, en_name, chap_list)
top_info.append(top)
ncx(root_path, novel_name, ncx_list)
opf(root_path, dc_info, item_info)
top_html(root_path, novel_name, top_info, True)
