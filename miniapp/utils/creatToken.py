# -*- coding: utf-8 -*-
# @Time    : 2022/2/4 14:22
# @Author  : kif
# @FileName: createToken.py
# @Software: PyCharm

import datetime

import jwt
from application.settings import SECRET_KEY

SALT = 'J4+opkLMck%W5pC3~^@YRGDmR&Du&E~9ObDVt$p)psyk#v'


def creattoken(user_data):
    # 构造header
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    # 构造payload

    payload = {
        'openid': user_data['openid'],
        'session_key': user_data['session_key'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=24 * 60)  # 超时时间
    }
    return jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
