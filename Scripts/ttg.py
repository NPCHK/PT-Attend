#!/usr/bin/env python3
#coding=utf8
import datetime
import os
import re
import requests
import sys
import time
from bs4 import BeautifulSoup

_COOKIE = ''

_USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
_URL = 'https://totheglory.im/signed.php'

if __name__ == '__main__':
    print("=======TTG=======")
    s = requests.Session()
    s.headers.update({'Cookie': _COOKIE,'User-Agent': _USERAGENT})

    try:
        homepage = s.get('https://totheglory.im/').text
        timestamp = re.search(r'signed_timestamp:\ \"[0-9]{10}\"', homepage).group()[19:29]
        token = re.search(r'signed_token:\ \".*?\"', homepage).group()[15:-1]
        payload = {'signed_timestamp': timestamp,'signed_token': token}
        r = s.post(_URL, data = payload)
    except Exception as e:
        print(e)
        sys.exit(1)

    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    open(dirname + "/.ttg.py", "w").close() 
    print("Status Code: " + str(r.status_code))
