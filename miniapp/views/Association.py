#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：backend 
@File    ：Association.py
@Author  ：kif<kif101001000@163.com>
@Date    ：2022/10/28 13:14 
'''
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from miniapp.models import *
from miniapp.serializers import miniappUserModelserializers, Associationserializer, bloodSugarSerializer, \
    periodicalLoggingSerializer, dietRecordsSerializer, sportsRecordsSerializer
from miniapp.views.BloodSugarData import addIntegralHistory


class createAssociation(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userAId = request.data.get('userAId')
        userA = miniappUser.objects.filter(id=userAId, is_active=True).first()
        if not userA:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        userBId = request.data.get('userBId')
        userB = miniappUser.objects.filter(id=userBId, is_active=True).first()
        if not userB:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        if Association.objects.filter(userA=userA, userB=userB).first() or Association.objects.filter(userA=userB,
                                                                                                      userB=userA).first():
            res['data'] = '已关联'
            res['status'] = 400
            return JsonResponse(res)
        else:
            As = Association.objects.create(userA=userA, userB=userB, createUser=userA)
            res['data'] = '待对方同意'
            res['status'] = 200
            return JsonResponse(res)


class cancelAssociation(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId, is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        AssociationId = request.data.get('AssociationId')
        As = Association.objects.filter(Q(id=AssociationId, userA=user) | Q(id=AssociationId, userB=user)).first()
        if not As:
            res['data'] = '邀请不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            As.delete()
            res['data'] = '已取消关联'
            res['status'] = 200
            return JsonResponse(res)


class Audit(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request):
        res = {}
        userId = request.GET.get('userId')
        user = miniappUser.objects.filter(id=userId, is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        AssociationId = request.GET.get('AssociationId')
        As = Association.objects.filter(id=AssociationId, userB=user).first()
        if not As:
            res['data'] = '邀请不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            As.is_active = True
            As.save()
            tarObj = IntegralDetail.objects.filter(name='绑定监护人').first()
            if tarObj:
                As.userA.integral += tarObj.integral
                As.userA.save()
                As.userB.integral += tarObj.integral
                As.userB.save()
                addIntegralHistory(As.userA, tarObj)
                addIntegralHistory(As.userB, tarObj)
            else:
                res['data'] = '联系客服设置积分值'
                res['status'] = 400
                return JsonResponse(res)
            res['data'] = '已关联'
            res['status'] = 200
            return JsonResponse(res)


class searchUserForAssociation(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId, is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        mobile = request.data.get('mobile')
        # user2 = miniappUser.objects.filter(Q(mobile=mobile, is_active=True) & ~Q(id=userId)).first()
        user2 = miniappUser.objects.filter(
            Q(Q(mobile=mobile) | Q(username=mobile)) & ~Q(id=userId) & Q(is_active=True)).first()
        if not user2:
            res['data'] = '无用户'
            res['status'] = 400
            return JsonResponse(res)
        else:
            res['data'] = {
                'id': user2.id,
                'avatar': user2.avatar,
                'gender': user2.gender,
                "username": user2.username,
            }
            res['status'] = 200
            return JsonResponse(res)


class getMyAssociation(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request):
        res = {}
        userId = request.GET.get('userId')
        user = miniappUser.objects.filter(id=userId, is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        AsList = Association.objects.filter(Q(userA=user) | Q(userB=user)).all()
        data = Associationserializer(AsList, many=True).data
        res['data'] = data
        res['status'] = 200
        return JsonResponse(res)


class getHealthHistory(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request):
        res = {}
        userId = request.GET.get('userId')
        user = miniappUser.objects.filter(id=userId, is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            bloodSugarLevelsData = bloodSugarLevels.objects.filter(user=user).all() \
                                       .order_by('bloodSugarTime')[:7]
            periodicalLoggingData = periodicalLogging.objects.filter(user=user).all() \
                                        .order_by('periodicalTime')[:7]
            dietRecordsData = dietRecords.objects.filter(user=user).all() \
                                  .order_by('time')[:7]
            sportsRecordsData = sportsRecords.objects.filter(user=user).all() \
                                    .order_by('time')[:7]
            res['data'] = {
                'height': user.height,
                'weight': user.weight,
                'bloodType': user.bloodType,
                'avatar': user.avatar,
                "username": user.username,
                'bloodSugarLevelsData': bloodSugarSerializer(bloodSugarLevelsData, many=True).data,
                'periodicalLoggingData': periodicalLoggingSerializer(periodicalLoggingData, many=True).data,
                'dietRecordsData': dietRecordsSerializer(dietRecordsData, many=True).data,
                'sportsRecordsData': sportsRecordsSerializer(sportsRecordsData, many=True).data,
            }
            res['status'] = 200
            return JsonResponse(res)
