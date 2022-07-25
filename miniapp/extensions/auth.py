# -*- coding: utf-8 -*-
# @Time    : 2021/8/6 16:10
# @Author  : kif
# @FileName: auth.py
# @Software: PyCharm

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt import exceptions

SALT = 'J4+opkLMck%W5pC3~^@YRGDmR&Du&E~9ObDVt$p)psyk#v'


class JwtQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_TOKEN")
        # print(token)
        try:
            # verified_payload = jwt.decode(token, SALT, True)
            verified_payload = jwt.decode(token, key=SALT, verify=False, algorithms=['HS256'])
        except exceptions.ExpiredSignatureError:
            msg = 'token已失效'
            raise AuthenticationFailed({'code': 400, 'message': msg})
        except jwt.DecodeError:
            msg = 'token认证失败'
            raise AuthenticationFailed({'code': 400, 'message': msg})
        except jwt.InvalidTokenError:
            msg = '非法的token'
            raise AuthenticationFailed({'code': 400, 'message': msg})
        return (verified_payload, token)
