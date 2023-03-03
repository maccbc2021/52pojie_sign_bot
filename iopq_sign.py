# -- coding: utf-8 --

import sys
import urllib.parse
import requests
from pyquery import PyQuery as pq

if __name__ == '__main__':
    cookie_str = input("请输入cookie：\n")
    if not cookie_str:
        print("cookie不能为空")
        sys.exit()
    cookies = ''
    for i in cookie_str.split("; "):
        key = i.split("=")[0]
        if "cbCe_9255_sid" in key:
            cookies += "cbCe_9255_sid=" + urllib.parse.quote(i.split("=")[1]) + "; "
        if "cbCe_9255_saltkey" in key:
            cookies += "cbCe_9255_saltkey=" + urllib.parse.quote(i.split("=")[1]) + ";"
        if "cbCe_9255_auth" in key:
            cookies += "cbCe_9255_auth=" + urllib.parse.quote(i.split("=")[1]) + ";"
    headers = {
        'authority': 'www.iopq.net',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'referer': 'https://www.iopq.net/',
        "Cookie": cookies,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    response = requests.get('https://www.iopq.net/', headers=headers)
    response.encoding = 'gbk'
    doc = pq(response.text)
    print(doc('.vwmy').text(), doc('#extcreditmenu').text(), doc('#g_upmine').text())
