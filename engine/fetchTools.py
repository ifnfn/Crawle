#!env python3
# -*- coding: utf-8 -*-

import base64
import hashlib
import os
import shutil
import sys
import traceback
import zlib
import re
import pickle
import gzip

try:
    from urlparse import urlparse
    import urllib
    import httplib as http
    urlretrieve = urllib.urlretrieve
    import urllib2 as urllib
except:
    from urllib.parse import urlparse
    import urllib.request
    import http.client as http
    urlretrieve = urllib.request.urlretrieve

global headers

MAX_TRY = 3
socket_timeout = 300


class AEScoder():
    def __init__(self):
        self.__encryptKey = "iEpSxImA0vpMUAabsjJWug=="
        self.__key = base64.b64decode(self.__encryptKey)

    def encrypt(self, data):
        encrData = base64.b64encode(data)
        return encrData

    def decrypt(self, encrData):
        encrData = base64.b64decode(encrData)

        return encrData


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive': '115',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}

def fetch_httplib2(url, method='GET', data=None, headers={}):
    conn = urlparse(url)

    if conn.scheme == "https":
        connection = http.HTTPSConnection(conn.netloc, timeout=socket_timeout)
    else:
        connection = http.HTTPConnection(conn.netloc, timeout=socket_timeout)
    # connection.debuglevel = 1

    connection.request(method=method, url=conn.path + '?' +
                       conn.query, body=data, headers=headers)
    response = connection.getresponse()

    try:
        content_type = response.headers['content-type']
    except:
        content_type = ''
    try:
        location = response.headers['location']
    except:
        location = ''

    return response.getcode(), content_type, location, response.read(),


def get_cache(url):
    response = None

    filename = './cache/' + hashlib.md5(url.encode('utf8')).hexdigest().upper()
    exists = os.path.exists(filename)

    if not exists:
        filename2 = './cache-old/' + \
            hashlib.md5(url.encode('utf8')).hexdigest().upper()
        exists = os.path.exists(filename2)
        if exists:
            shutil.move(filename2, filename)
            exists = os.path.exists(filename)
    if exists:
        f = open(filename, 'rb')
        response = f.read()
        response = AEScoder().decrypt(response)
        f.close()
        # print(filename, url)

    return response, exists


def save_cache(url, response):
    if not response:
        return
    response = AEScoder().encrypt(response)
    filename = './cache/' + hashlib.md5(url.encode('utf8')).hexdigest().upper()
    try:
        f = open(filename, 'wb')
        f.write(response)
        f.close()
    except Exception as e:
        print(e)
        pass


def get_url(url, times=0):
    if times > MAX_TRY:
        return '', False
    try:
        status, _, _, response = fetch_httplib2(url)
        if status != 200 and status != 304 and status != 404:
            print('status %s, try %d, %s ...' % (status, times + 1, url))
            return get_url(url, times + 1)
        return response, True
    except:
        t, v, tb = sys.exc_info()
        print("get_url: %s %s, %s, %s" %
              (url, t, v, traceback.format_tb(tb)))
        return get_url(url, times + 1)


def post_url(url, header={}, data=None, cached=False, times=0):
    if times > MAX_TRY:
        return '', False
    try:
        status, _, _, response = fetch_httplib2(url, 'POST', data, header)
        if status != '200' and status != '304' and status != '404':
            print('status %s, try %d ...' % (status, times + 1))
            return post_url(url, header, data, cached, times + 1)
        return response, True
    except:
        print("try: ", url)
        return post_url(url, header, data, cached, times + 1)


def fetch(url, method, header={}, data=None, cached=False):
    exists = False
    response = None

    if cached:
        response, exists = get_cache(url)

    if method == None:
        method = "GET"

    if not exists:
        if method.upper() == "POST":
            response, exists = post_url(url, header, data, cached)
        else:
            response, exists = get_url(url)
        if exists:
            save_cache(url, response)
    return response, exists


def RegularMatch(regular, text):
    x = ''
    for r in regular:
        res = re.finditer(r, text)
        if (res):
            for i in res:
                if type(i.group(1)) == bytes:
                    x += i.group(1).decode("GB18030") + '\n'
                else:
                    x += i.group(1) + '\n'
            text = x
    if x:
        x = x[0:len(x) - 1]
    return x


def RegularMatchUrl(url, regular):
    response, _ = fetch(url, "GET", cached=True)
    # 对数据 response 转码
    coding = 'utf8'
    try:
        if type(response) == bytes:
            response = response.decode(coding)
    except:
        coding = 'GB18030'
        if type(response) == bytes:
            response = response.decode(coding)

    return RegularMatch([regular], response)


if __name__ == '__main__':
    # url = 'http://store.tv.sohu.com/view_content/movie/5008825_704321.html'
    # url = 'http://index.tv.sohu.com/index/switch-aid/1012657'
    # url = 'http://www.kolatv.com/'
    # _, _, _, response = fetch_httplib2(url)
    # print(response.decode())

    # url = "http://127.0.0.1:8080/get"
    url = "https://sokindle.com/books/4660.html"
    data = "e_secret_key=523523"

    header = {}
    header["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36"
    header["Content-Type"] = "application/x-www-form-urlencoded"

    response, found = fetch(url, "GET", cached=False)
    print(response.decode())

    response, found = fetch(url, "POST", header, data, False)
    # response, responses = conn.request(
    #     uri=url, method="POST", body=data, headers=header)
    # try:
    #     content_type = response['content-type']
    # except:
    #     content_type = ''
    print(response.decode())


def data_save(filename, *objects):
    with gzip.open(filename, 'wb') as fil:
        for obj in objects:
            pickle.dump(obj, fil)


def data_load(filename):
    with gzip.open(filename, 'rb') as fil:
        while True:
            try:
                return pickle.load(fil)
            except EOFError:
                break
