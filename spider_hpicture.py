from concurrent.futures import ThreadPoolExecutor
import requests
import logging
from queue import Queue
import threading
from lxml import etree
from bs4 import BeautifulSoup
import time


bak = "https://bbs.hupu.com/27175199.html"

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT,level=logging.INFO)

headers = {
    "User-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

base_url = "https://bbs/selfie"
second_url = "https://bbs/"

urls_queue = Queue()
second_urls_queue = Queue()
htmls_queue = Queue()
outputs_queue = Queue()

event = threading.Event()

def create_urls(start,end,step=1):
    for i in range(start,end+1,step):
        urls_queue.put('{}-{}'.format(base_url,i))
    print("url create successful")

def create_second_urls():
    while not event.is_set():
        try:
            url = urls_queue.get(True,1)
            with requests.get(url,headers=headers) as response:
                content = response.text
                html = etree.HTML(content)
                rewrite_url = html.xpath("//div[@class='titlelink box']/a/@href")
                for i in rewrite_url:
                    # complete_second_url = second_url+i
                    second_urls_queue.put('{}{}'.format(second_url,i))
        except Exception as e:
            logging.error(e)



def crawler():
    while not event.is_set():
        try:
            url = second_urls_queue.get(True,1)
            with requests.get(url,headers=headers) as response:
                html = response.text
                htmls_queue.put(html)
                print(url)
        except:
            pass

def parser():
    while not event.is_set():
        try:
            content = htmls_queue.get(True,1)
            html = etree.HTML(content)
            rewrite_url = html.xpath("//div[@id='tpc']//img/@src")
            for img in rewrite_url:
                if img.endswith('webp'):
                    outputs_queue.put(img)
        except Exception as e:
            logging.error(e)

def save():
    file_num = 1
    while not event.is_set():
        try:
            img = outputs_queue.get(True,1)
            file_num+=1

            with open(str(file_num) + '.webp', 'wb') as fd:
                picture = requests.get(img).content
                fd.write(picture)

        except Exception as e:
            logging.error(e)


executor = ThreadPoolExecutor(10)
executor.submit(create_urls,1,2)
executor.submit(create_second_urls)
executor.submit(parser)
executor.submit(save)
for i in range(7):
    executor.submit(crawler)

while True:
    inp = input('please stop:')
    if inp.strip() == 'quit':
        event.set()
        print('stoping')
        time.sleep(4)
        break
