# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os



options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'E:\\0'}
options.add_experimental_option('prefs', prefs)
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(chrome_options=options)
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': 'E:\\0'}}
command_result = driver.execute("send_command", params)
driver.get('http://www.wuqimh.com/655/')
url_soups = driver.find_elements_by_class_name('status0')
url_soups.reverse()
chap_urls = list(map(lambda x: x.get_attribute('href'), url_soups))
for chap_url in chap_urls:
    driver.get(chap_url)
    page_nos = driver.find_element_by_id('pageSelect').find_elements(By.TAG_NAME, 'option')
    page_nos = list(map(lambda x: x.get_attribute('value'), page_nos))[1:]
    chap_name = driver.find_element(By.TAG_NAME, 'h2').text
    for i in page_nos:
        image_url = chap_url+'?p='+i
        driver.get(image_url)
        img_src = driver.find_element_by_id('manga').get_attribute('src')
        if not os.path.exists('E:\\0\\%s' % chap_name):
            os.mkdir('E:\\0\\%s' % chap_name)
        try:
            req = requests.get(img_src)
            name = '%03d' % int(i)
            if req.status_code == 200:
                with open('E:\\0\\%s\\%s.jpg' % (chap_name,name), 'wb') as fp:
                    fp.write(req.content)
        except Exception:
            continue

driver.quit()
