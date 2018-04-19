#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: get_cartoons.py
@time: 2018/4/18 下午5:19

"""
import os
import re
import json
import requests
import base64
import multiprocessing

search_url = 'http://ac.qq.com/Comic/search/word/{}'
book_url = 'http://ac.qq.com/Comic/comicInfo/id/{}'
video_list = 'http://m.ac.qq.com/GetData/getComicInfo?id={}'
chapter_url = 'http://m.ac.qq.com/GetData/getChapterList?id={}'
img_url = 'http://ac.qq.com/ComicView/index/id/{0}/seqno/{1}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/63.0.3239.84 Safari/537.36'}
current_dir = os.path.dirname(os.path.realpath(__file__))


def check_dir(full_dir):
    if not os.path.exists(full_dir):
        os.makedirs(full_dir)


class SpiderComic(object):

    def __init__(self):
        super().__init__()
        self.book_name = ''
        self.book_id = ''
        self.book_des = ''
        self.book_len = 0

    def down_comic(self, book_name):
        self.book_id = SpiderComic.get_list_by_book_name(book_name)[0][0]
        info = SpiderComic.get_list_video(self.book_id)
        self.book_name = info['title'].strip()
        self.book_des = info['brief_intrd']
        chapter = SpiderComic.get_chapter(self.book_id)
        self.book_len = chapter['length']
        for i in range(self.book_len):
            print('开始下载第{}章'.format(i+1))
            process = multiprocessing.Process(target=SpiderComic.down_img, args=(i+1, self.book_id))
            process.start()

    @staticmethod
    def get(url, char_set='utf-8'):
        session = requests.session()
        resp = session.get(url, headers=headers, stream=True, verify=False)
        resp.encoding = char_set
        return resp

    @staticmethod
    def get_list_by_book_name(name):
        resp = SpiderComic.get(search_url.format(name))
        try:
            text = resp.text
            tips_list = text.split('\n')
            items = list(map(lambda x: x.split('|'), tips_list))
            return items
        except Exception as e:
            print(e)

    @staticmethod
    def get_list_video(book_id):
        resp = SpiderComic.get(video_list.format(book_id))
        try:
            text = resp.text
            msg = json.loads(text)
            return msg
        except Exception as e:
            print(e)

    @staticmethod
    def get_chapter(book_id):
        resp = SpiderComic.get(chapter_url.format(book_id))
        try:
            text = resp.text
            chapter = json.loads(text)
            """
            {'last':'417','1':{'t':'1.姐姐','n':'2', 'p':'1'or None, seq:0,eid:KkNLWi4=,v:2},...,length:343}
            """
            return chapter
        except Exception as e:
            print(e)

    @staticmethod
    def down_img(chapter_id, book_id):
        global img_url
        resp = SpiderComic.get(img_url.format(book_id, chapter_id))
        try:
            text = resp.text
            pattern = r'DATA\s*=\s*\'(.*)\''
            list_data = re.findall(pattern, text)
            if len(list_data):
                str_info = str(base64.b64decode(list_data[0][1:]), 'utf-8')
                img_detail = json.loads(str_info)
                book_title = img_detail['comic']['title']
                c_title = img_detail['chapter']['cTitle']
                print(book_title, c_title)
                download_dir = '{}/../download/{}/{}/'.format(current_dir, book_title, c_title)
                check_dir(download_dir)
                for i, _v in enumerate(img_detail['picture']):
                    img_url = _v['url']
                    img_name = '{}{}.jpg'.format(download_dir, i)
                    SpiderComic.down_file(img_url, img_name)
        except Exception as e:
            print(e)

    @staticmethod
    def down_file(url, file):
        resp = SpiderComic.get(url)
        print(file)
        print('开始下载...')
        try:
            with open(file, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            print('下载完成')
        except Exception as e:
            print('下载出错:', e)


def main():
    SpiderComic().down_comic('一人之下')


if __name__ == '__main__':
    main()

