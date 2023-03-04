# -- coding: utf-8 --

import requests
import re
from bs4 import BeautifulSoup

SESSION = requests.Session()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

BASE_URL = "https://www.jiaofs.com"


def get_formhash():
    url = f"{BASE_URL}/plugin.php?id=k_misign:sign"
    response = SESSION.get(url=url, headers=HEADERS)
    response.raise_for_status()  # 判断请求状态是否正常
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("input", {"name": "formhash"})["value"]


# 从原始cookie中解析包含_saltkey或_auth的cookie
def parse_cookie(raw_cookie):
    pattern = r"(\S+)(_saltkey|_auth)=(\S+);"
    matches = re.findall(pattern, raw_cookie)
    cookies = {}
    for match in matches:
        cookies[match[0] + match[1]] = match[2]
    return cookies


def sign(formhash):
    sign_url = f"{BASE_URL}/plugin.php?id=k_misign:sign&operation=qiandao&format=button&formhash={formhash}&inajax=1&ajaxtarget=midaben_sign"
    sign_resp = SESSION.get(url=sign_url, headers=HEADERS)
    sign_resp.raise_for_status()  # 判断请求状态是否正常
    soup = BeautifulSoup(sign_resp.text, 'xml')
    cdata = soup.find('root').string
    print(cdata)


if __name__ == "__main__":
    try:
        input_cookie = input("请输入jiaofs.com cookie的值：\r\n").strip()
        cookies = parse_cookie(input_cookie)
        SESSION.cookies.update(cookies)
        formhash = get_formhash()
        sign(formhash)
    except requests.exceptions.RequestException as e:
        print(e)
