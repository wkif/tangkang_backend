import time

from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework import serializers

from dvadmin.utils.validator import CustomUniqueValidator
from miniapp.serializers import addressSerializer
from shop.models import *


# SKU
class SKUModelserializers(CustomModelSerializer):
    comments = serializers.SerializerMethodField()

    # brand = serializers.SerializerMethodField()

    #
    def get_comments(self, obj):
        data = obj.skucommits_set.all().filter(is_delete=False).order_by('-add_time')
        print(data)
        return SKUCommitsModelserializers(data, many=True).data
        # return obj.category.name


    # def get_brand(self, obj):
    #     return obj.brand.name

    class Meta:
        model = SKU
        fields = '__all__'


class SKUModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = SKU
        fields = '__all__'


class SKUserializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'


# 商品分类

class goodsCategoryModelserializers(CustomModelSerializer):
    class Meta:
        model = goodsCategory
        fields = '__all__'


class goodsCategoryModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = goodsCategory
        fields = '__all__'


class goodsCategoryserializer(serializers.ModelSerializer):
    class Meta:
        model = goodsCategory
        fields = '__all__'


# 品牌
class BrandModelserializers(CustomModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = Brand
        fields = '__all__'


class Brandserializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


# 评论
class SKUCommitsModelserializers(CustomModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'avatar': obj.user.avatar,
        }

    class Meta:
        model = SKUCommits
        fields = '__all__'


# 订单
class OrderInfoModelserializers(CustomModelSerializer):
    user = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    good = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'avatar': obj.user.avatar,
            'name': obj.user.name,
            'mobile': obj.user.mobile,
        }

    def get_address(self, obj):
        return addressSerializer(obj.address).data

    def get_good(self, obj):
        return SKUserializer(obj.good).data

    def get_order_status(self, obj):
        list = ["待支付", "待发货", "待收货", "待评价", "已完成", "已取消"]
        return list[obj.order_status - 1]

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoModelCreateSerializer(CustomModelSerializer):
    """
    创建时的列化器
    """

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoModelUpdateSerializer(CustomModelSerializer):
    """
    更新时的列化器
    """

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoserializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = '__all__'
