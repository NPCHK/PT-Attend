#!/usr/bin/env python3
#coding=utf8
import os
import requests
import sys
from bs4 import BeautifulSoup

_COOKIE = ''
_URL = 'https://pt.gztown.net/attendance.php'

if __name__ == '__main__':
    s = requests.Session()
    s.headers.update({'Cookie': _COOKIE})

    print("=======GZT=======")
    try:
        r = s.get(_URL)
    except Exception as e:
        print(e)
        sys.exit(1)

    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    open(dirname + "/.gzt.py", "w").close
    print("Status Code: " + str(r.status_code))
