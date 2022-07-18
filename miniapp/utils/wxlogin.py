# -*- coding: utf-8 -*-
# @Time    : 2022/2/3 20:01
# @Author  : kif
# @FileName: wx_login.py
# @Software: PyCharm
from application.settings import code2Session, AppId, AppSecret
import requests


def get_login_info(code):
    code_url = code2Session.format(AppId, AppSecret, code)
    response = requests.get(code_url)
    json_response = response.json()  # 把它变成json的字典
    if json_response.get("session_key"):
        return json_response
    else:
        return False
