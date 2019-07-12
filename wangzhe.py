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
            r.encoding = 'gbk'
            if r.status_code != 200:
                print('***' + url)
                continue
            return BeautifulSoup(r.text, 'lxml')
        except BaseException:
            traceback.print_exc()
            continue


noveurl = 'http://www.wutuxs.com/html/5/5579/'
rootUrl = 'http://www.wutuxs.com/'
top_info = []
novel_name = re.sub('\W', '', '王者')
urls = [noveurl]
root_path = 'D:\\jin\\' + novel_name
ncx_list = []
dc_info = dict()
dc_info['Title'] = novel_name
dc_info['Language'] = 'zh-CN'
dc_info['Creator'] = '寻飞'
dc_info['Copyrights'] = 'zrc'
dc_info['Publisher'] = 'zrc'
item_info = list()
for novel_url in urls:
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    top_soup = get_content(novel_url)
    en_name = 'wangzhe'
    book_name = novel_name
    print(novel_name + '--->' + book_name)
    top = {'book_title': book_name, 'book_url': en_name + '.html', 'child_tops': []}
    ncx_map = {'text': book_name, 'src': en_name + '.html', 'child': []}

    item_info.append({'id': en_name, 'href': en_name + '.html'})
    chap_list = []
    i = 1
    top_soup_list = top_soup.select('[id="at"] a')
    for chap_url_soup in top_soup_list:
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
        content_str = content_soup.select_one('[id="contents"]').text.strip()
        content_list = re.split('\s{2,}',content_str)
        for chap_soup in content_list:
            chap_content.append(chap_soup)
        chap['content'] = chap_content
        chap_list.append(chap)
        i += 1
    ncx_list.append(ncx_map)
    content_html(root_path, en_name, chap_list)
    top_info.append(top)
ncx(root_path, novel_name, ncx_list)
opf(root_path, dc_info, item_info)
top_html(root_path, novel_name, top_info, True)