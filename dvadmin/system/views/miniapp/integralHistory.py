#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：backend 
@File    ：integralHistory.py
@Author  ：kif<kif101001000@163.com>
@Date    ：2022/10/29 20:22 
'''
from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import integralHistory
from miniapp.serializers import integralHistoryModelserializers, integralHistoryModelCreateUpdateSerializer


class integralHistoryModelViewset(CustomModelViewSet):
    queryset = integralHistory.objects.all()
    serializer_class = integralHistoryModelserializers
    create_serializer_class = integralHistoryModelCreateUpdateSerializer
    update_serializer_class = integralHistoryModelCreateUpdateSerializer

