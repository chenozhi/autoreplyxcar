import pytesseract
from PIL import Image
import datetime
import time
from bs4 import BeautifulSoup
import requests

def request_download():

    #http://114.115.233.109/inc/code.php?t=Thu May 30 2019 21:14:11 GMT+0800 (中国标准时间)
    ti = time.strftime("%a %b %d %Y %H:%M:%S ", time.localtime())
    para = ti + 'GMT+0800 (中国标准时间)'

    print(para)
    r = requests.Session().get('http://114.115.233.109/inc/code.php?t=%s' % (ti))
    with open('./code.png', 'wb') as f:
        f.write(r.content)

    image = Image.open('code.png')
    text = pytesseract.image_to_string(image)
    print(text)

    cookie = 'PHPSESSID=74a32933af05a1f156973b559e06be83'
    header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
              'Accept - Encoding': 'gzip, deflate',
             'content-type': 'application/x-www-form-urlencoded',
              'cookie':cookie,
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    params = {'time': ti, 'name': '成都'.encode('utf-8'), 'code': text, 'button': 'button'}

    resp = requests.Session().post(url='http://114.115.233.109/?t=%s' % (ti), data=params, headers=header)
    resp.encoding = 'gb2312'
    html = resp.text
    print(html)
    return para

def cookie_to_dict(cookie):
    cookie_dict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        cookie_dict[key] = value
    return cookie_dict

para = request_download()

