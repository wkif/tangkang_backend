from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings

from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from miniapp.models import *


class JfwTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(JfwTokenObtainPairSerializer, cls).get_token(user)
        token['id'] = 'wx_{0}'.format(user.id)
        t = (token.access_token)
        a = api_settings.USER_ID_CLAIM
        user_id = t[a]
        flag = 1
        user_model = get_user_model(flag)
        u = user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        if u:
            u.last_login = datetime.now()
            u.save()
        else:
            user_model.objects.create(**{api_settings.USER_ID_FIELD: user_id})
        return token


class miniappUserModelserializers(CustomModelSerializer):
    class Meta:
        model = miniappUser
        exclude = ["password"]


class miniappUserModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = miniappUser
        fields = ["is_active"]


class userserializer(serializers.ModelSerializer):
    class Meta:
        model = miniappUser
        exclude = ["password", "is_active", 'openid']
        # fields = '__all__'


#

class foodDatabaseModelserializers(CustomModelSerializer):
    class Meta:
        model = foodDatabase
        fields = '__all__'


class foodDatabaseModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = foodDatabase
        fields = '__all__'


class foodDatabaseserializer(serializers.ModelSerializer):
    class Meta:
        model = foodDatabase
        fields = '__all__'


# 用户协议
class userAgreementModelserializers(CustomModelSerializer):
    class Meta:
        model = userAgreement
        fields = '__all__'


class userAgreementModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = userAgreement
        fields = '__all__'


class userAgreementserializer(serializers.ModelSerializer):
    class Meta:
        model = userAgreement
        fields = '__all__'


# 公告

class announcementbaseModelserializers(CustomModelSerializer):
    class Meta:
        model = announcement
        fields = '__all__'


class announcementbaseModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = announcement
        fields = '__all__'


class announcementbaseserializer(serializers.ModelSerializer):
    class Meta:
        model = announcement
        fields = '__all__'


class foodDatabaseModelserializers(CustomModelSerializer):
    class Meta:
        model = foodDatabase
        fields = '__all__'


class foodDatabaseModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = foodDatabase
        fields = '__all__'


class foodDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = foodDatabase
        fields = '__all__'


# 地址
class addressSerializer(serializers.ModelSerializer):
    class Meta:
        model = address
        fields = '__all__'


class bloodSugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = bloodSugarLevels
        fields = '__all__'


class periodicalLoggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = periodicalLogging
        fields = '__all__'
