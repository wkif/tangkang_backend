#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：backend 
@File    ：Association.py
@Author  ：kif<kif101001000@163.com>
@Date    ：2022/10/29 15:03 
'''
from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import Association
from miniapp.serializers import AssociationModelserializers, AssociationModelCreateUpdateSerializer


class AssociationModelViewset(CustomModelViewSet):
    queryset = Association.objects.all()
    serializer_class = AssociationModelserializers
    create_serializer_class = AssociationModelCreateUpdateSerializer
    update_serializer_class = AssociationModelCreateUpdateSerializer

    # queryset = miniappUser.objects.all()
    # serializer_class = miniappUserModelserializers
