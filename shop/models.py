from django.db import models

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
    desc = models.CharField(max_length=200, verbose_name='描述')
    detail = models.TextField(verbose_name='详情')
    image = models.CharField(null=True, blank=True, verbose_name='商品图片', max_length=200)
    imgList = models.CharField(null=True, blank=True, verbose_name='商品图片列表', max_length=500)
    stock = models.IntegerField(default=0, verbose_name='库存')
    sales = models.IntegerField(default=0, verbose_name='销量')
    comments = models.IntegerField(default=0, verbose_name='评价数')
    status = models.SmallIntegerField(default=0, choices=SPU_STATUS_CHOICES)

    class Meta:
        db_table = daName + 'tb_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
