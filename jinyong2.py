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
            proxy = {'https': 'http://192.168.80.88:8080', 'http': 'http://192.168.80.88:8080'}
            r = requests.request('get', url, headers=headers, proxies=proxy)

            # time.sleep(random.randint(3, 4))
            r.encoding = 'utf-8'
            if r.status_code != 200:
                print('***' + url)
                continue
            return BeautifulSoup(r.text, 'lxml')
        except BaseException:
            traceback.print_exc()
            continue


print(get_content(
    'https://hr.synnex-china.com/scripts/mgrqispi.dll?appname=hrsoft2000&prgname=Addressbook_StaffDetail&arguments=-AS0203371723978,-A8801'))
