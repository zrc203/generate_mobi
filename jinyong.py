import requests
import traceback
from bs4 import BeautifulSoup
import os
from gen_ncx import ncx
from gen_opf import opf
from gen_top_html import top_html
from gen_content import content_html
import time


def get_content(url):
    try:
        r = requests.request('get', url)
        r.encoding = 'utf-8'
        if r.status_code != 200:
            time.sleep(10)
            print('***'+url)
            return get_content(url)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    except BaseException:
        traceback.print_exc()
        return get_content(url)


rootUrl = 'http://www.jinyongwang.com/'
for novel_url in get_content(rootUrl).select('[class="book_li_other"] a'):
    root_path = 'D:\\jin\\' + novel_url.text
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    top_soup = get_content(rootUrl + novel_url['href'])
    en_name = novel_url['href'].split('/')[-2]
    book_name = top_soup.select_one('font[class="phonenone"]').text
    chap_list = []
    for chap_url_soup in top_soup.select('[class="mlist"] a'):
        chap_name = chap_url_soup.text
        content_soup = get_content(rootUrl + chap_url_soup['href'])
        chap = dict()
        chap['chap_name'] = chap_name
        print(chap_name)
        chap_content = []
        for chap_soup in content_soup.select('[id="vcon"] p'):
            chap_content.append(chap_soup.text)
        chap['content'] = chap_content
        chap_list.append(chap)
        break
    content_html(root_path, en_name, chap_list)

ncx(root_path, ncx_title, ncx_list)
opf(root_path, dc_info, item_info)
top_html(root_path, '金庸修订版', top_info, True)

