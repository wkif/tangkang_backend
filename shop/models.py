import datetime
import random
import time

from django.db import models
from miniapp.models import *

# Create your models here.
daName = 'shop_'


class goodsCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    desc = models.CharField(max_length=200)
    parent = models.ForeignKey('self', related_name='subs', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='父类别')

    class Meta:
        db_table = daName + 'tb_goods_category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    desc = models.CharField(max_length=200)

    class Meta:
        db_table = daName + 'tb_brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


SPU_STATUS_CHOICES = (
    (0, '下架'),
    (1, '上架'),
)


class SKU(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='名称')
    caption = models.CharField(max_length=100, verbose_name='副标题')
    category = models.ForeignKey(goodsCategory, on_delete=models.CASCADE, verbose_name='商品类别')
    brand = models.ForeignKey('brand', on_delete=models.CASCADE, verbose_name='品牌')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    # desc = models.CharField(max_length=200, verbose_name='描述')
    detail = models.TextField(verbose_name='详情')
    image = models.CharField(null=True, blank=True, verbose_name='商品图片', max_length=200)
    imgList = models.CharField(null=True, blank=True, verbose_name='商品图片列表', max_length=500)
    stock = models.IntegerField(default=0, verbose_name='库存')
    sales = models.IntegerField(default=0, verbose_name='销量')
    comments = models.JSONField(null=True, blank=True, verbose_name='评价', max_length=1000)
    status = models.SmallIntegerField(default=0, choices=SPU_STATUS_CHOICES)
    recommended = models.BooleanField(default=False, verbose_name='是否推荐')

    class Meta:
        db_table = daName + 'tb_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class SKUCommits(models.Model):
    id = models.AutoField(primary_key=True)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    user = models.ForeignKey('miniapp.miniappUser', on_delete=models.CASCADE)
    score = models.SmallIntegerField(default=5, null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)


def order_uuid():
    """
        :return: 20220525140635467912
        :PS ：并发较高时尾部随机数增加
    """
    order_id = str(datetime.datetime.fromtimestamp(time.time())).replace("-", "").replace(" ", "").replace(":",
                                                                                                           "").replace(
        ".", "") + str(random.randint(100, 999))
    return order_id


class OrderInfo(models.Model):
    # 订单状态
    ORDER_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECEIVED": 3,
        "UNCOMMENT": 4,
        "FINISHED": 5
    }
    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价"),
        (5, "已完成"),
        (6, "已取消"),
    )
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=64, unique=True, default=order_uuid, verbose_name='订单号')
    user = models.ForeignKey('miniapp.miniappUser', on_delete=models.CASCADE, verbose_name='用户')
    address = models.ForeignKey('miniapp.address', on_delete=models.CASCADE, verbose_name='地址')
    good = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='商品', null=True, blank=True)
    total_count = models.IntegerField(default=1, verbose_name='商品数量', null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价', null=True, blank=True)
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费', null=True, blank=True)
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    trade_no = models.CharField(max_length=128, null=True, blank=True, verbose_name='支付编号')
    tracking_number = models.CharField(max_length=128, null=True, blank=True, verbose_name='物流单号')
    update_datetime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = daName + 'tb_order_info'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name
