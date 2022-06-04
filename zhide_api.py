# coding=utf-8
import base64
import hashlib

import requests
import traceback
import threading
import random
import time
import os
from math import floor

from Crypto.Cipher import AES

from gen.gen_ncx import ncx
from gen.gen_opf import opf
from gen.gen_top_html import top_html
from gen.gen_content import content_html
import re
import json

# 搜索 https://s.lansheweb.com/v1/lists.api?keyword=最佳女婿
# 详情 https://book.lansheweb.com/details/154/154192.html
# 目录 https://catalog.lansheweb.com/ai/128/1c/38/35.html
# 正文 https://chapter.lansheweb.com/ai/128/1c/38/35/1.html


def get_content(url):
    while True:
        try:
            md = hashlib.md5()
            times = str(round(time.time()))
            s = f"com.ruffianhankin.meritreader1{times}vhjJVz1St6tK7!8n#B0MqRIuE2Dh7!C#"
            md.update(s.encode())
            sign = str(md.hexdigest())
            headers = {"package": "com.ruffianhankin.meritreader", "pt": "1", "time": times, "sign": sign,
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53"}
            r = requests.request('get', url, headers=headers, verify=False)
            r.encoding = 'utf-8'
            if r.status_code != 200:
                print('***' + url)
                continue
            text = r.text
            return json.loads(text)
        except BaseException as e:
            time.sleep(random.randint(3, 4))
            traceback.print_exc()
            continue


class AESCipher:
    def __init__(self, secretkey: str):
        self.key = secretkey  # 密钥
        self.iv = 'E&z!EHGLd$fli*8R'  # 偏移量

        self.DEFAULT = 0  # 默认模式, 每行不超过76个字符
        self.NO_PADDING = 1  # 移除最后的=
        self.NO_WRAP = 2  # 不换行，一行输出
        self.CRLF = 4  # 采用win上的换行符
        self.URL_SAVE = 8  # 采用urlsafe

    def decode(self, content: str, flag: int) -> bytes:
        missing_padding = len(content) % 4
        if missing_padding != 0:
            content = content.ljust(len(content) + (4 - missing_padding), "=")

        if flag & self.URL_SAVE:
            result = base64.urlsafe_b64decode(content.encode("utf-8"))
        else:
            result = base64.b64decode(content.encode("utf-8"))
        return result

    def decrypt(self, encrypted_text):
        """
        解密 ：偏移量为key[0:16]；先base64解，再AES解密，后取消补位
        :param encrypted_text : 已经加密的密文
        :return:
        """
        encrypted_text = self.decode(encrypted_text, self.NO_WRAP)
        cipher = AES.new(key=self.key.encode(), mode=AES.MODE_CBC, IV=self.iv.encode())
        decrypted_text = cipher.decrypt(encrypted_text)
        return decrypted_text.decode('utf-8')


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
            chap_name = AESCipher('Pxga!h*e4@T8xfOm').decrypt(chap_url_soup['name'])
            chap_name = re.sub('[\x00-\xff]+$', '', chap_name)

            if not chap_url_soup['is_content']:
                print(f'{chap_name} not find')
                continue
            print(chap_name)
            content_soup = get_content(f'https://chapter.lansheweb.com/{chap_url_soup["path"]}')
            chap = dict()
            chap['chap_name'] = chap_name
            chap['idx'] = chap_url_soup['idx']
            content_list = AESCipher('Pxga!h*e4@T8xfOm').decrypt(content_soup['data']['content'])
            chap_content = re.sub('[\x00-\xff]*', '', content_list)
            chap_content = re.split('\s{2,}', chap_content)
            chap_content = list(filter(lambda x: x!='', chap_content))
            chap['content'] = chap_content
            chap['url'] = chap_url_soup["path"]
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
    book_id = 3113
    noveurl = f'https://book.lansheweb.com/details/{floor(book_id / 1000)}/{book_id}.html'
    # noveurl = f'https://s.lansheweb.com/v1/lists.api?keyword=造化之门'
    top_soup = get_content(noveurl)
    novel_name = top_soup['data']['name']
    en_name = 'qugekongjie'
    root_path = 'D:\\jin\\' + novel_name
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    chap_soup = get_content(f'https://book.lansheweb.com/source/{floor(book_id / 1000)}/{book_id}.html')
    site_path = chap_soup['data'][2]['site_path']
    chap_list_soup = get_content(f'https://catalog.lansheweb.com/{site_path}')
    top_soup_list = chap_list_soup['data']
    dc_info = dict()
    dc_info['Title'] = novel_name
    dc_info['Language'] = 'zh-CN'
    dc_info['Creator'] = 'zrc'
    dc_info['Copyrights'] = 'zrc'
    dc_info['Publisher'] = top_soup['data']['author']
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
