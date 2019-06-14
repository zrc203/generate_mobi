import requests
import traceback
from bs4 import BeautifulSoup
import os
from gen_ncx import ncx
from gen_opf import opf
from gen_top_html import top_html
from gen_content import content_html
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


xiuding = 'http://jinyongxiaoshuo.com/xiuding'
rootUrl = 'http://jinyongxiaoshuo.com/'
top_info = []
urls = get_content(xiuding).select('dd a')
root_path = 'D:\\jin\\修订版'
ncx_list = []
dc_info = dict()
dc_info['Title'] = '修订版'
dc_info['Language'] = 'zh-CN'
dc_info['Creator'] = 'zrc'
dc_info['Copyrights'] = 'zrc'
dc_info['Publisher'] = 'zrc'
item_info = list()
for novel_url in urls:
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    top_soup = get_content(rootUrl + novel_url['href'])
    en_name = novel_url['href'].split('/')[-2]
    book_name = novel_url.select_one('b').text
    print(book_name)
    top = {'book_title': book_name, 'book_url': en_name + '.html', 'child_tops': []}
    ncx_list.append({'text': book_name, 'src': en_name + '.html'})
    item_info.append({'id': en_name, 'href': en_name + '.html'})
    chap_list = []
    i = 1
    top_soup_list = top_soup.select('dd a')
    if book_name.startswith('射雕英雄') or book_name.startswith('雪山飞狐'):
        top_soup_list.reverse()
    for chap_url_soup in top_soup_list:
        chap_name = chap_url_soup.text
        content_soup = get_content(chap_url_soup['href'])
        chap = dict()
        chap['chap_name'] = chap_name
        child_top = {'chap_url': chap_name, 'chap_title': en_name + '.html#%s' % i}
        top['child_tops'].append(child_top)
        ncx_list.append({'text': chap_name, 'src': en_name + '.html#%s' % i})
        print(chap_name)
        chap_content = []
        content_list = content_soup.select('div[class="entry"] p')
        for chap_soup in content_list:
            if 'JinYongXiaoShuo' in chap_soup.text:
                break
            chap_content.append(chap_soup.text)
        chap['content'] = chap_content
        chap_list.append(chap)
        i += 1
    content_html(root_path, en_name, chap_list)
    top_info.append(top)
ncx(root_path, u'金庸修订版', ncx_list)
opf(root_path, dc_info, item_info)
top_html(root_path, u'金庸修订版', top_info, True)
