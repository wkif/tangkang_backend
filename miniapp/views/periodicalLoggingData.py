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




# 定期记录--------------------------------------------------------start

class getperiodicalLoggingDataByUserId(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        periodicalLoggingData = periodicalLogging.objects.filter(user=user).all().order_by('periodicalTime')
        if not periodicalLoggingData:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        res['data'] = periodicalLoggingSerializer(periodicalLoggingData, many=True).data
        res['status'] = 200
        return JsonResponse(res)


class addPeriodicalLoggingData(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        periodicalTime = request.data.get('periodicalTime')
        glycosylatedHemoglobin = request.data.get('glycosylatedHemoglobin')
        microalbuminuria = request.data.get('microalbuminuria')
        dorsalisPedisArtery = request.data.get('dorsalisPedisArtery')
        if not periodicalTime or not glycosylatedHemoglobin or not microalbuminuria or not dorsalisPedisArtery:
            res['data'] = '请填写完整信息'
            res['status'] = 400
            return JsonResponse(res)
        periodicalLogging.objects.create(user=user, periodicalTime=periodicalTime,
                                         glycosylatedHemoglobin=glycosylatedHemoglobin,
                                         microalbuminuria=microalbuminuria, dorsalisPedisArtery=dorsalisPedisArtery)
        res['data'] = '添加成功'
        res['status'] = 200
        return JsonResponse(res)


class deletePeriodicalLoggingData(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        periodicalLoggingId = request.data.get('periodicalLoggingId')
        periodicalLogg = periodicalLogging.objects.filter(id=periodicalLoggingId).first()
        if not periodicalLogg:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        periodicalLogg.delete()
        res['data'] = '删除成功'
        res['status'] = 200
        return JsonResponse(res)


# 定期记录--------------------------------------------------------end