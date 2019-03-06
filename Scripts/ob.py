#!/usr/bin/env python3
#coding=utf8
import os
import requests
import sys
from bs4 import BeautifulSoup

_COOKIE = ''
_URL = 'https://ourbits.club/attendance.php'

if __name__ == '__main__':
    print("=======OB========")
    s = requests.Session()
    s.headers.update({'Cookie': _COOKIE})

    try:
        r = s.get(_URL)
    except Exception as e:
        print(e)
        sys.exit(1)

    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    open(dirname + "/.ob.py", "w").close()
    print("Status Code: " + str(r.status_code))
