#!/usr/bin/env python3
#coding=utf8
import datetime
import os
import requests
import sys
import time
from bs4 import BeautifulSoup

_COOKIE = ''

_TIMESTAMP = int(time.time())
_USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
_URL = 'https://www.hdarea.co/sign_in.php'

if __name__ == '__main__':
    print("=======hda=======")
    s = requests.Session()
    s.headers.update({'Cookie': _COOKIE, 'User-Agent': _USERAGENT})

    try:
        r = s.post(_URL, data = {'action': 'sign_in'})
    except Exception as e:
        print(e)
        sys.exit(1)

    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    open(dirname + "/.hda.py", "w").close()
    print("Status Code: " + str(r.status_code))
