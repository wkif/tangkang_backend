import json
from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings

from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from miniapp.models import *


# 后台管理端======================================================start

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
    foodType = serializers.SerializerMethodField()

    def get_foodType(self, obj):
        # print(obj.foodType)
        list = ['蔬菜', '水果', '肉类', '蛋类', '奶类', '鱼类', '豆类', '谷物', '其他']
        return list[obj.foodType]

    class Meta:
        model = foodDatabase
        fields = '__all__'


# 积分

class integralDetailModelserializers(CustomModelSerializer):
    class Meta:
        model = IntegralDetail
        fields = '__all__'


class integralDetailModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = IntegralDetail
        fields = '__all__'


class integralDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegralDetail
        fields = '__all__'


# 资讯
class newsModelserializers(CustomModelSerializer):
    is_delete = serializers.SerializerMethodField()
    top = serializers.SerializerMethodField()

    def get_is_delete(self, obj):
        if obj.is_delete:
            return '已删除'
        else:
            return '未删除'

    def get_top(self, obj):
        if obj.top:
            return '是'
        else:
            return '否'

    class Meta:
        model = news
        fields = '__all__'


class newsModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = news
        fields = '__all__'


class newsserializer(serializers.ModelSerializer):
    class Meta:
        model = news
        fields = '__all__'


# 評論
class commitOfNewsModelserializers(CustomModelSerializer):
    news = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    is_delete = serializers.SerializerMethodField()

    def get_news(self, obj):
        return newsModelserializers(obj.news).data

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'avatar': obj.user.avatar,
        }

    def get_is_delete(self, obj):
        if obj.is_delete:
            return '已删除'
        else:
            return '未删除'

    class Meta:
        model = commitOfNews
        fields = '__all__'


class commitOfNewsModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = commitOfNews
        fields = '__all__'


class commitOfNewsserializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'avatar': obj.user.avatar
        }

    class Meta:
        model = commitOfNews
        fields = '__all__'


# 页面路径

class pagePathListModelserializers(CustomModelSerializer):
    class Meta:
        model = pagePathList
        fields = '__all__'


class pagePathListCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = pagePathList
        fields = '__all__'


class pagePathListSerializer(serializers.ModelSerializer):
    class Meta:
        model = pagePathList
        fields = '__all__'


# 底部tab

class tabListModelserializers(CustomModelSerializer):
    class Meta:
        model = tabList
        fields = '__all__'


class tabListCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = tabList
        fields = '__all__'


class tabListSerializer(serializers.ModelSerializer):
    class Meta:
        model = tabList
        fields = '__all__'


# 后台管理端======================================================end


# 小程序端======================================================start
# 小程序端======================================================end


# 地址
class addressSerializer(serializers.ModelSerializer):
    class Meta:
        model = address
        fields = '__all__'


# 血糖记录
class bloodSugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = bloodSugarLevels
        fields = '__all__'


# 不定期记录

class periodicalLoggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = periodicalLogging
        fields = '__all__'


# 饮食记录
class dietRecordsSerializer(serializers.ModelSerializer):
    # food = serializers.SerializerMethodField()
    #
    # def get_food(self, obj):
    #     # food = json.loads(obj.food)
    #     for item in obj.food:
    #         list = ['蔬菜', '水果', '肉类', '蛋类', '奶类', '鱼类', '豆类', '谷物', '其他']
    #         item['food']['foodType'] = list[int(item['food']['foodType'])]
    #     return obj.food

    class Meta:
        model = dietRecords
        fields = '__all__'


class integralHistorySerializer(serializers.ModelSerializer):
    integralType = serializers.SerializerMethodField()

    def get_integralType(self, obj):
        return {
            'type': integralDetailSerializer(obj.integralType).data['name'],
            'integral': integralDetailSerializer(obj.integralType).data['integral']
        }

    class Meta:
        model = integralHistory
        fields = '__all__'


class sportsRecordsSerializer(serializers.ModelSerializer):
    sportstype = serializers.SerializerMethodField()
    user=serializers.SerializerMethodField()

    def get_sportstype(self, obj):
        return {
            "name": obj.sportstype.name,
            "id": obj.sportstype.id
        }
    def get_user(self,obj):
        return obj.user.username

    class Meta:
        model = sportsRecords
        fields = '__all__'
class sportsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = sportsType
        fields = '__all__'