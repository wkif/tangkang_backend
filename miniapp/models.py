import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from dvadmin.system.views.admin import user
from dvadmin.utils.models import CoreModel, table_prefix
from dvadmin.system.models import *

STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
)
bloodSugarType_CHOICES = (
    (0, "空腹血糖"),
    (1, "早餐后2小时血糖"),
    (2, "午餐前血糖"),
    (3, "午餐后2小时血糖"),
    (4, "晚餐前血糖"),
    (5, "晚餐后2小时血糖"),
    (6, "睡前血糖"),
    (7, "任意时间血糖"),
    (8, "夜间2时血糖"),
    (9, "其他"),
)

foodType_CHOICES = (
    (0, "蔬菜"),
    (1, "水果"),
    (2, "肉类"),
    (3, "蛋类"),
    (4, "奶类"),
    (5, "鱼类"),
    (6, "豆类"),
    (7, "谷物"),
    (8, "其他"),
)

daName = 'miniapp_'


# 用户信息区=====================================================================================================================


class miniappUser(models.Model):
    """
    用户表
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name="用户账号", help_text="用户账号")
    password = models.CharField(u'密码', max_length=50, default='123456')
    email = models.EmailField(max_length=255, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True, help_text="电话")
    avatar = models.CharField(max_length=255, verbose_name="头像", null=True, blank=True, help_text="头像")
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")
    GENDER_CHOICES = (
        (2, "未知"),
        (0, "男"),
        (1, "女"),
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="性别", null=True, blank=True, help_text="性别"
    )
    height = models.CharField(u'身高', max_length=50, default='160', null=True, blank=True)
    weight = models.CharField(u'体重', max_length=50, default='110', null=True, blank=True)
    birthday = models.DateField(u'生日', null=True, blank=True)
    bloodType = models.CharField(u'血型', max_length=50, default='A', null=True, blank=True)
    waistline = models.CharField(u'腰围', max_length=50, default='80', null=True, blank=True)
    openid = models.CharField(max_length=255, default='', null=True, blank=True)
    userStatement = models.CharField(u'介绍', max_length=150, default="", null=True, blank=True)
    is_active = models.BooleanField(u'可用数据', default=True)
    userRegDate = models.DateField('注册日期', auto_now_add=True)
    realNameAuthentication = models.BooleanField(u'实名认证', default=False)
    realName = models.CharField(u'真实姓名', max_length=50, default='', null=True, blank=True)
    ID_number = models.CharField(u'身份证号', max_length=50, default='', null=True, blank=True)
    inviteCode = models.CharField(u'邀请码', max_length=50, default='', null=True, blank=True)
    numberofPersonsInvited = models.IntegerField(u'邀请人数', default=0)
    speed = models.BooleanField(u'是否语音播报', default=False)
    integral = models.IntegerField(u'积分', default=0)

    def set_password(self, raw_password):
        super().set_password(hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest())

    class Meta:
        db_table = daName + "users"
        verbose_name = "小程序用户表"
        verbose_name_plural = verbose_name


# 血糖目标表
class bloodGlucoseTargetValue(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(miniappUser, on_delete=models.CASCADE)
    bloodSugar0_targetValue = models.FloatField(verbose_name="空腹血糖目标值")
    bloodSugar1_targetValue = models.FloatField(verbose_name="早餐后2小时血糖目标值")
    bloodSugar2_targetValue = models.FloatField(verbose_name="午餐前血糖目标值")
    bloodSugar3_targetValue = models.FloatField(verbose_name="午餐后2小时血糖目标值")
    bloodSugar4_targetValue = models.FloatField(verbose_name="晚餐前血糖目标值")
    bloodSugar5_targetValue = models.FloatField(verbose_name="晚餐后2小时血糖目标值")
    bloodSugar6_targetValue = models.FloatField(verbose_name="睡前血糖目标值")
    bloodSugar7_targetValue = models.FloatField(verbose_name="任意时间血糖目标值")
    bloodSugar8_targetValue = models.FloatField(verbose_name="夜间2时血糖目标值")
    bloodSugar9_targetValue = models.FloatField(verbose_name="其他血糖目标值")
    createDate = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updateDate = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = daName + "bloodGlucoseTargetValue"
        verbose_name = "血糖目标值"
        verbose_name_plural = verbose_name


# 用户地址表
class address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(miniappUser, on_delete=models.CASCADE)
    name = models.CharField(u'收货人', max_length=50, default='', null=True, blank=True)
    phone = models.CharField(u'手机号', max_length=50, default='', null=True, blank=True)
    baseAddress = models.CharField(u'基础地址', max_length=50, default='', null=True, blank=True)
    address = models.CharField(u'地址', max_length=50, default='', null=True, blank=True)
    postalCode = models.CharField(u'邮编', max_length=50, default='', null=True, blank=True)
    isDefault = models.BooleanField(u'是否默认', default=False)

    class Meta:
        db_table = daName + "address"
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name


# 用户信息区=====================================================================================================================

# 血糖记录表
class bloodSugarLevels(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(miniappUser, on_delete=models.CASCADE)
    bloodSugarLevel = models.FloatField(u'血糖', default=0)
    bloodSugarTime = models.DateTimeField(u'血糖时间', null=True, blank=True)
    bloodSugarType = models.IntegerField(
        choices=bloodSugarType_CHOICES, default=0, verbose_name="血糖类型", null=True, blank=True, help_text="血糖类型"
    )
    STATUS_CHOICES = (
        (0, "不达标"),
        (1, "达标"),
    )
    status = models.IntegerField(u'状态', choices=STATUS_CHOICES, default=0, help_text="状态")

    class Meta:
        db_table = daName + "bloodSugarLevels"
        verbose_name = "血糖日记录"
        verbose_name_plural = verbose_name


# 不定期记录表
class periodicalLogging(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(miniappUser, on_delete=models.CASCADE)
    periodicalTime = models.DateTimeField(u'日期', null=True, blank=True)
    glycosylatedHemoglobin = models.FloatField(u'糖化血红蛋白', default=0)
    microalbuminuria = models.FloatField(u'微量白蛋白', default=0)
    dorsalisPedisArtery = models.CharField(u'足跟静脉搏动', max_length=50, default='', null=True, blank=True)

    class Meta:
        db_table = daName + "periodicalLogging"
        verbose_name = "日常记录"
        verbose_name_plural = verbose_name


# **行为记录**

# 食品参数表
class foodDatabase(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.CharField(u'图片', max_length=250,
                           default='https://kifimg.oss-cn-beijing.aliyuncs.com/project/202205151948902.png', null=True,
                           blank=True)
    foodName = models.CharField(u'食物名称', max_length=50, default='', null=True, blank=True)
    foodType = models.IntegerField(
        choices=foodType_CHOICES, default=0, verbose_name="食物类型", null=True, blank=True, help_text="食物类型"
    )
    unit = models.CharField(u'单位', max_length=50, default='', null=True, blank=True)
    foodCalory = models.FloatField(u'卡路里', default=0)
    foodProtein = models.FloatField(u'蛋白质', default=0)
    foodFat = models.FloatField(u'脂肪', default=0)
    foodCarbohydrate = models.FloatField(u'碳水化合物', default=0)
    foodVitaminA = models.FloatField(u'维生素A', default=0)
    foodVitaminC = models.FloatField(u'维生素C', default=0)
    foodVitaminE = models.FloatField(u'维生素E', default=0)
    foodVitaminD = models.FloatField(u'维生素D', default=0)
    heat = models.FloatField(u'热量', default=0)

    class Meta:
        db_table = daName + "foodDatabase"
        verbose_name = "食物库"
        verbose_name_plural = verbose_name


# 饮食记录表
class dietRecords(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(miniappUser, on_delete=models.CASCADE)
    time = models.DateTimeField(u'日期', null=True, blank=True)
    food = models.JSONField(u'食物', default='', null=True, blank=True)
    foodCalory = models.FloatField(u'卡路里', default=0)
    foodProtein = models.FloatField(u'蛋白质', default=0)
    foodFat = models.FloatField(u'脂肪', default=0)
    foodCarbohydrate = models.FloatField(u'碳水化合物', default=0)
    foodVitaminA = models.FloatField(u'维生素A', default=0)
    foodVitaminC = models.FloatField(u'维生素C', default=0)
    foodVitaminE = models.FloatField(u'维生素E', default=0)
    foodVitaminD = models.FloatField(u'维生素D', default=0)
    heat = models.FloatField(u'热量', default=0)

    class Meta:
        db_table = daName + "dietRecords"
        verbose_name = "饮食记录"
        verbose_name_plural = verbose_name


class sportsType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u'名称', max_length=50, default='', null=True, blank=True)
    heat = models.FloatField(u'热量', default=0)


# 运动记录表
class sportsRecords(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(miniappUser, on_delete=models.CASCADE)
    startTime = models.DateTimeField(u'开始时间', null=True, blank=True)
    endTime = models.DateTimeField(u'结束时间', null=True, blank=True)
    time = models.DateTimeField('记录日期', auto_now_add=True)
    sportstype = models.ForeignKey(sportsType, on_delete=models.CASCADE)
    heat = models.FloatField(u'热量', default=0)


# 系统区============================================================系统区


# 公告表
class announcement(models.Model):
    id = models.AutoField(primary_key=True)
    createUser = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="announcement_createUser")
    release = models.BooleanField(u'是否发布', default=False)
    title = models.CharField(u'标题', max_length=50, default='', null=True, blank=True)
    content = models.TextField(u'内容', default='', null=True, blank=True)
    createTime = models.DateTimeField(u'创建时间', auto_now_add=True)
    updateTime = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        db_table = daName + "announcement"
        verbose_name = "公告"
        verbose_name_plural = verbose_name


# 用户协议表
class userAgreement(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(u'内容', default='', null=True, blank=True)
    createTime = models.DateTimeField(u'创建时间', auto_now_add=True)
    updateTime = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        db_table = daName + "userAgreement"
        verbose_name = "用户协议"
        verbose_name_plural = verbose_name


# 积分明细表
class IntegralDetail(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u'名称', max_length=50, default='', null=True, blank=True)
    integral = models.IntegerField(u'积分', default=0)
    createTime = models.DateTimeField(u'创建时间', auto_now_add=True)
    updateTime = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        db_table = daName + "IntegralDetail"
        verbose_name = "积分分类明细"
        verbose_name_plural = verbose_name


class integralHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(miniappUser, on_delete=models.CASCADE)
    integralType = models.ForeignKey(IntegralDetail, on_delete=models.CASCADE)
    integral = models.IntegerField(u'积分', default=0, null=True, blank=True)
    time = models.DateTimeField(u'时间', auto_now_add=True)

    class Meta:
        db_table = daName + "integralHistory"
        verbose_name = "积分记录明细"
        verbose_name_plural = verbose_name


# 资讯
class news(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(u'标题', max_length=50, default='', null=True, blank=True)
    content = models.TextField(u'内容', default='', null=True, blank=True)
    tag = models.CharField(u'标签', max_length=50, default='', null=True, blank=True)
    createTime = models.DateTimeField(u'创建时间', auto_now_add=True)
    updateTime = models.DateTimeField(u'更新时间', auto_now=True)
    is_delete = models.BooleanField(u'是否删除', default=False)
    top = models.BooleanField(u'是否置顶', default=False)
    cover = models.CharField(null=True, blank=True, verbose_name='封面', max_length=200)

    class Meta:
        db_table = daName + "news"
        verbose_name = "资讯"
        verbose_name_plural = verbose_name


class commitOfNews(models.Model):
    id = models.AutoField(primary_key=True)
    news = models.ForeignKey(news, on_delete=models.CASCADE)
    user = models.ForeignKey(miniappUser, on_delete=models.CASCADE)
    content = models.TextField(u'内容', default='', null=True, blank=True)
    time = models.DateTimeField(u'时间', auto_now_add=True)
    is_delete = models.BooleanField(u'是否删除', default=False)

    class Meta:
        db_table = daName + "commitOfNews"
        verbose_name = "资讯评论"
        verbose_name_plural = verbose_name


class pagePathList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u'名称', max_length=50, default='', null=True, blank=True)
    path = models.CharField(u'路径', max_length=50, default='', null=True, blank=True)

    class Meta:
        db_table = daName + "pagePathList"
        verbose_name = "页面路径"
        verbose_name_plural = verbose_name


class tabList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u'名称', max_length=50, default='', null=True, blank=True)
    pagePath = models.ForeignKey(pagePathList, on_delete=models.CASCADE)
    iconPath = models.CharField(null=True, blank=True, verbose_name='默认图标', max_length=200)
    selectedIconPath = models.CharField(null=True, blank=True, verbose_name='选中图标', max_length=200)
    is_active = models.BooleanField(u'是否展示', default=True)

    class Meta:
        db_table = daName + "tabList"
        verbose_name = "底部导航栏"
        verbose_name_plural = verbose_name


class hotSearch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u'名称', max_length=50, default='', null=True, blank=True)
    count = models.IntegerField(u'次数', default=0)

    class Meta:
        db_table = daName + "hotSearch"
        verbose_name = "热搜"
        verbose_name_plural = verbose_name
