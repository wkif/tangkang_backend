"""provision URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path

from miniapp.views import *

urlpatterns = [
    # 基础功能
    path('login/', loginApi.as_view()),
    path('getUserAgreement/', getUserAgreement.as_view()),
    # 收货地址
    path('getAddressByUsrid/', getAddressByUsrid.as_view()),
    path('addAddressByUserid/', addAddressByUserid.as_view()),
    path('deleteAddressByUserid/', deleteAddressByUserid.as_view()),
    path('editAddress/', editAddress.as_view()),

    # 用户信息
    path('getUserInfoByUserId/', getUserInfoByUserId.as_view()),
    path('editUserInfo/', editUserInfo.as_view()),
    path('realnameAuthentication/', realnameAuthentication.as_view()),
    #     公告
    path('getTopNoticeData/', getTopNoticeData.as_view()),
    path('getNoticeData/', getNoticeData.as_view()),
    #     血糖值日记录
    path('getBloodSugarDataByUserId/', getBloodSugarDataByUserId.as_view()),
    path('getLastBloodSugarDataByUserId/', getLastBloodSugarDataByUserId.as_view()),
    path('addBloodSugarData/', addBloodSugarData.as_view()),
    path('deleteBloodSugarData/', deleteBloodSugarData.as_view()),
    #     定期记录
    path('getperiodicalLoggingDataByUserId/', getperiodicalLoggingDataByUserId.as_view()),
    path('addPeriodicalLoggingData/', addPeriodicalLoggingData.as_view()),
    path('deletePeriodicalLoggingData/', deletePeriodicalLoggingData.as_view()),
#     食物数据库
    path('getfoodDatabase/', getfoodDatabase.as_view()),

]
