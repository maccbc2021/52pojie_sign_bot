# -- coding: utf-8 --

import requests
import urllib.parse
import re
from bs4 import BeautifulSoup
import notify

SESSION = requests.Session()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

BASE_URL = "https://bbs.125.la"


def get_formhash():
    url = f"{BASE_URL}/plugin.php?id=dsu_paulsign:sign"
    response = SESSION.get(url=url, headers=HEADERS)
    print(response.text)
    response.raise_for_status()  # 判断请求状态是否正常
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("input", {"name": "formhash"})["value"]


# 从原始cookie中解析包含_saltkey或_auth的cookie
def parse_cookie(raw_cookie):
    pattern = r"(\S+)(_saltkey|_auth)=(\S+);"
    matches = re.findall(pattern, raw_cookie)
    cookies = {}
    for match in matches:
        cookies[match[0] + match[1]] = urllib.parse.quote(match[2], safe='')
    return cookies


def sign(formhash):
    sign_url = f"{BASE_URL}/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1"
    data = {
        "formhash": formhash,
        "submit": "1",
        "targerurl": "",
        "todaysay": "",
        "qdxq": "kx"
    }
    sign_resp = SESSION.post(url=sign_url, data=data, headers=HEADERS)
    sign_resp.raise_for_status()  # 判断请求状态是否正常
    text = sign_resp.json()['msg']
    print(text)
    notify.send("精益论坛签到", text)


if __name__ == "__main__":
    try:
        input_cookie = input("请输入bbs.125.la cookie的值：\r\n").strip()
        cookies = parse_cookie(input_cookie)
        SESSION.cookies.update(cookies)
        formhash = get_formhash()
        sign(formhash)
    except requests.exceptions.RequestException as e:
        print(e)
