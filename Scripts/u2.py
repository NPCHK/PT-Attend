#!/usr/bin/env python3
#coding=utf8
import cv2
import os
import numpy as np
import re
import requests
import sys
import time
from bs4 import BeautifulSoup
from urllib.request import quote

_Proxies = {}
#_Proxies = {'http': 'http://127.0.0.1:10086', 'https': 'http://127.0.0.1:10086'} 
# 如果本机可以直接访问Google，则本项留空
# 如果本机在墙内，请填入http代理，形如{'http': 'http://127.0.0.1:10086', 'https': 'http://127.0.0.1:10086'}，注意http和https都要填写
_COOKIE = ''
# 填入你的u2 cookie，可以在Chrome的F12里Request Headers里找到

_USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
_URL = 'https://u2.dmhy.org/showup.php?action=show'
_MESSAGE = '回答按钮点击时即提交，手滑损失自负~'
_Current_DIR, _Filename = os.path.split(os.path.abspath(sys.argv[0]))

def Google_Search(cvIMG, Time):
    Filename = Time+'.png'
    cv2.imwrite(Filename, cvIMG)
    Upload_URL = 'https://www.google.com/searchbyimage/upload'
    response = requests.post(Upload_URL, proxies = _Proxies, files={'encoded_image': (Filename,open(Filename,'rb')), 'hl': 'ja'}, allow_redirects=False)
    Search_URL = response.headers['Location']
    # print(Search_URL)

    # Use Google Image Search
    search = requests.Session()
    search.headers.update({'User-Agent': _USERAGENT})
    search.proxies = _Proxies

    try:
        rs = search.get(Search_URL)
        soup = BeautifulSoup(rs.text, "html5lib")
    except Exception as e:
        print(e)
        return("")

    try:
        Guess = str(soup.find_all(name='div', attrs={"class": "SPZz6b"})[0].find("span"))[6:-7]
        #print("Guess: "+Guess)
        return(Guess)
    except Exception as e:
        Guess = ""

    try:
        TMP = re.search(r'他のキーワード候補.*?\<\/a\>', rs.text).group()
        #TMP = re.search(r'Possible\ related\ search.*?\<\/a\>', rs.text).group()
        Guess = re.search(r'\"\>.*?\<\/a\>', TMP).group()[2:-4]
        #print("Guess: "+Guess)
        return(Guess)
    except Exception as e:
        print(e)
        return("")
    return("")

def SplitIMG(CaptchaURL):
    Mean = 100
    # Request the Captcha 2 times to calc the difference,
    # the change of pictures' order will results a relatively high average brightness in the difference graph-> retry 
    while(Mean>9):
        imgReq = requests.get(CaptchaURL)
        img = cv2.imdecode(np.asarray(bytearray(imgReq.content), dtype=np.uint8), cv2.IMREAD_COLOR)
        imgReq = requests.get(CaptchaURL)
        img2 = cv2.imdecode(np.asarray(bytearray(imgReq.content), dtype=np.uint8), cv2.IMREAD_COLOR)
        # Calculate difference graph.
        sminus = cv2.cvtColor(cv2.subtract(img,img2), cv2.COLOR_RGB2GRAY)
        Mean = sminus.mean()
        #cv2.imshow("2 times",sminus[:-50][:])
        #cv2.waitKey(0)

    # Use Canny Algorithm to find the edge and split the img.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #blur = cv2.GaussianBlur(gray,(3,3),0)
    blur = gray
    canny = cv2.Canny(blur, 100, 500)
    #cv2.imshow("canny",canny)
    #cv2.waitKey(0)

    height, width = canny.shape
    flag = 1
    hmax = 0
    wmax = 0

    # Find the boundary between 2 pictures, from vertical and horizontal.
    for j in range(3, width-3): # Bypass the original edge.
        TMP = 0
        for i in range(0, height):
            if (canny[i][j-1]>0 or canny[i][j]>0 or canny[i][j+1]>0):
                TMP = TMP + 1
        if (TMP > hmax):
            hmax = TMP
            hpos = j
    #print(hpos, hmax/height)
    for i in range(3, height-3):
        TMP = 0
        for j in range(0, width):
            if (canny[i-1][j]>0 or canny[i][j]>0 or canny[i+1][j]>0):
                TMP = TMP + 1
        if (TMP > wmax):
            wmax = TMP
            wpos = i
    #print(wpos, wmax/width)
    if (hmax/height > wmax/width):
        pos = hpos
        flag = 1
    else:
        pos = wpos
        flag = 0

    Status = 1
    if (flag):
        pic_a = img[:,hpos+1:]
        pic_b = img[:,:hpos-1]
        pic_a_minus = sminus[:-50,hpos+1:]
        pic_b_minus = sminus[:-50,:hpos-1]
        #
        if(pic_a_minus.mean()>0.01):
            return(pic_a,1)
        else:
            return(pic_b,1)
    else:
        # Just bypass the horizontal boundary because there's no bother to try it again :P
        return([],0)

def LCS(s1, s2):
    m=[[0 for i in range(len(s2)+1)]  for j in range(len(s1)+1)]
    mmax=0
    p=0
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i]==s2[j]:
                m[i+1][j+1]=m[i][j]+1
                if m[i+1][j+1]>mmax:
                    mmax=m[i+1][j+1]
                    p=i+1
    return s1[p-mmax:p],mmax

if __name__ == '__main__':
    print("=======U2========")
    s = requests.Session()
    s.headers.update({'Cookie': _COOKIE,'User-Agent': _USERAGENT})
    Success = 0
    while(Success==0):
        Recognize = 0
        try:
            while(Recognize==0):
                CurrentTime = int(time.time())
                showup_page = s.get('https://u2.dmhy.org/showup.php').text
                CaptchaIMG = "https://u2.dmhy.org/" + re.search(r'<img src=\"image.php\?action=adbc2\&.*?\"', showup_page).group()[10:-1]

                Pic, Recognize = SplitIMG(CaptchaIMG)
                if(Recognize==1):
                    Pic_name = Google_Search(Pic, str(CurrentTime))
                    #cv2.imshow("Pic", Pic)
                    #cv2.waitKey(0)
                    os.remove(str(CurrentTime)+".png")

                    req = re.search(r'name=\"req\" value=\".*?\"', showup_page).group()[18:-1]
                    imghash = re.search(r'name=\"hash\" value=\".*?\"', showup_page).group()[19:-1]
                    form = re.search(r'name=\"form\" value=\".*?\"', showup_page).group()[19:-1]
                    submit_list = re.findall(r'type=\"submit\" name=\".*?\" value=\"[\s\S]*?\"', showup_page)

                    captcha_name = []
                    captcha_value = []
                    anime_name = []
                    LCS_MAX = 0
                    for i in range(0,4):
                        captcha_value.append(re.search(r'value=\"[\s\S]*?\"', submit_list[i]).group()[7:-1])
                        submit_list[i] = submit_list[i].replace("\n","")
                        captcha_name.append(re.search(r'name=\".*?\"', submit_list[i]).group()[6:-1])
                        anime_name.append(re.search(r'value=\".*?\"', submit_list[i]).group()[7:-1])

                        LCS_String, LCS_Length = LCS(anime_name[i].lower(),Pic_name.lower())
                        if(LCS_Length > LCS_MAX):
                            LCS_MAX = LCS_Length
                            ans = i

                    if(LCS_MAX<=3):
                        Recognize = 0
                        # If the max LCS was too short, we doubt that the Google Search may response with a null result or some other errors occured, try agian.
                    else:
                        Recognize = 1
                        print(anime_name[ans])
                        payload = {'message': _MESSAGE, 'req': req, 'hash': imghash, 'form': form, captcha_name[ans]: captcha_value[ans]}

                        r = s.post(_URL, data = payload)
                        Success = 1
        except Exception as e:
            #print(e)
            print("Trying again...")

    print("Status Code: " + str(r.status_code))
    open(_Current_DIR + "/.u2.py", "w").close()

