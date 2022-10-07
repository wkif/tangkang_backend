import datetime
import json
import re
from random import choice
from string import ascii_uppercase as uc, digits as dg
import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.tokens import RefreshToken

from dvadmin.utils.permission import CustomPermission
from miniapp.extensions.auth import JwtQueryParamsAuthentication
from miniapp.models import *
from miniapp.serializers import userserializer, addressSerializer, JfwTokenObtainPairSerializer, bloodSugarSerializer, \
    periodicalLoggingSerializer, announcementbaseserializer, foodDatabaseSerializer, dietRecordsSerializer, \
    integralHistorySerializer, newsserializer, commitOfNewsserializer, sportsRecordsSerializer, sportsTypeSerializer
from miniapp.utils.checkIdnum import check_id_data
from miniapp.utils.creatToken import creattoken
from miniapp.utils.wxlogin import get_login_info
from rest_framework_simplejwt.views import TokenObtainPairView

from shops.models import SKU, OrderInfo, goodsCategory
from shops.serializers import SKUModelserializers, OrderInfoModelserializers

class getUserAgreement(APIView):
    # authentication_classes = ()  # 在此重新定义认证方式
    # permission_classes = ()  # 在此重新定义权限

    def get(self, request):
        res = {}
        UserAgreement = userAgreement.objects.all().order_by('-id')
        if UserAgreement:
            content = UserAgreement.first().content
            res['data'] = {
                'content': content,
                'createTime': UserAgreement.first().createTime,
                'updateTime': UserAgreement.first().updateTime

            }

        else:
            res['data'] = '暂无内容'
        res['status'] = 200
        return JsonResponse(res)

class getTabList(APIView):
    def get(self, request):
        res = {}
        tablist = tabList.objects.filter(is_active=True).all()
        list = []
        for item in tablist:
            list.append({
                'name': item.name,
                'selectedIconPath': item.selectedIconPath,
                'iconPath': item.iconPath,
                'pagePath': item.pagePath.path
            })
        res['data'] = list
        res['status'] = 200
        return JsonResponse(res)

class changespeed(APIView):
    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            if user.speed:
                user.speed = False
            else:
                user.speed = True
            user.save()
            res['data'] = '修改成功'
            res['status'] = 200
            return JsonResponse(res)


class getSpeed(APIView):
    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            if user.speed:
                res['data'] = 1
                res['status'] = 200
                return JsonResponse(res)
            else:
                res['data'] = 0
                res['status'] = 200
                return JsonResponse(res)
