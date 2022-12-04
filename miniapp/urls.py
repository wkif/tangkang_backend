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

from miniapp.views.Association import createAssociation, searchUserForAssociation, getMyAssociation, Audit, \
    getHealthHistory, cancelAssociation
from miniapp.views.BloodSugarData import getBloodSugarDataByUserId, addBloodSugarData, deleteBloodSugarData, \
    getLastBloodSugarDataByUserId
from miniapp.views.Integral import getIntegralHistory
from miniapp.views.Notice import getTopNoticeData, getNoticeData
from miniapp.views.Sports import addSportsRecords, deleteSportsRecordsByid, dailySportList, getsportsType, \
    getSportsRecordsByid
from miniapp.views.Target import addBloodGlucoseTargetValue, getBloodGlucoseTargetValue, addSportTargetValue, \
    getSportTargetValue, addFoodTargetValue, getFoodTargetValue
from miniapp.views.Base_View import getUserAgreement, getTabList, changespeed, getSpeed
from miniapp.views.Food_Database import getfoodDatabase, getDietRecords, getfoodDatabaseByname, deleteDietRecords, \
    addDietRecords
from miniapp.views.News import getNewsList, getCommitOfNews, addCommit, getNewsDetail, deleteCommit, getTopNews, \
    searchNews, getHotSearch, getStatusOfLike, LikeOfNews, addShareOfNews, addViewOfNews
from miniapp.views.Periodical_Logging_Data import getperiodicalLoggingDataByUserId, deletePeriodicalLoggingData, \
    addPeriodicalLoggingData
from miniapp.views.Shops import getShopList, getMyOrderList, cancelOrder, addOrder, getTopGoods, getGoodDetail, payment, \
    confirmOrder, addCommitById, getOrderById

from miniapp.views.User import loginApi, getAddressByUsrid, addAddressByUserid, deleteAddressByUserid, editAddress, \
    editUserInfo, getUserInfoByUserId, realnameAuthentication, getUserIntegral

urlpatterns = [
    # 基础功能
    path('login/', loginApi.as_view()),
    path('getUserAgreement/', getUserAgreement.as_view()),
    path('getTabList/', getTabList.as_view()),
    # 语音开关
    path('changespeed/', changespeed.as_view()),
    path('getspeed/', getSpeed.as_view()),
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
    path('getfoodDatabaseByname/', getfoodDatabaseByname.as_view()),
    path('getDietRecords/', getDietRecords.as_view()),
    path('addDietRecords/', addDietRecords.as_view()),
    path('deleteDietRecords/', deleteDietRecords.as_view()),

    # 积分记录
    path('getIntegralHistory/', getIntegralHistory.as_view()),
    path('getUserIntegral/', getUserIntegral.as_view()),

    #     shop
    path('getShopList/', getShopList.as_view()),
    path('addOrder/', addOrder.as_view()),
    path('getMyOrderList/', getMyOrderList.as_view()),
    path('cancelOrder/', cancelOrder.as_view()),
    path('getTopGoods/', getTopGoods.as_view()),
    path('getGoodDetail/', getGoodDetail.as_view()),
    path('payment/', payment.as_view()),
    path('confirmOrder/', confirmOrder.as_view()),
    path('addCommitById/', addCommitById.as_view()),
    path('getOrderById/', getOrderById.as_view()),

    #     资讯
    path('getNewsList/', getNewsList.as_view()),
    path('getNewsDetail/', getNewsDetail.as_view()),
    path('getNewsComment/', getCommitOfNews.as_view()),
    path('addCommit/', addCommit.as_view()),
    path('deleteCommit/', deleteCommit.as_view()),
    path('getTopNews/', getTopNews.as_view()),
    path('searchNews/', searchNews.as_view()),
    path('getHotSearch/', getHotSearch.as_view()),
    path('getStatusOfLike/', getStatusOfLike.as_view()),
    path('LikeOfNews/', LikeOfNews.as_view()),
    path('addShareOfNews/', addShareOfNews.as_view()),
    path('addViewOfNews/', addViewOfNews.as_view()),
    #     运动记录
    path('addSportsRecords/', addSportsRecords.as_view()),
    path('getSportsRecordsByid/', getSportsRecordsByid.as_view()),
    path('deleteSportsRecordsByid/', deleteSportsRecordsByid.as_view()),
    path('dailySportList/', dailySportList.as_view()),
    path('getsportsType/', getsportsType.as_view()),
    #     目标
    path('addBloodGlucoseTargetValue/', addBloodGlucoseTargetValue.as_view()),
    path('getBloodGlucoseTargetValue/', getBloodGlucoseTargetValue.as_view()),
    path('addSportTargetValue/', addSportTargetValue.as_view()),
    path('getSportTargetValue/', getSportTargetValue.as_view()),
    path('addFoodTargetValue/', addFoodTargetValue.as_view()),
    path('getFoodTargetValue/', getFoodTargetValue.as_view()),

    #     关联
    path('createAssociation/', createAssociation.as_view()),
    path('cancelAssociation/', cancelAssociation.as_view()),
    path('searchUserForAssociation/', searchUserForAssociation.as_view()),
    path('getMyAssociation/', getMyAssociation.as_view()),
    path('Audit/', Audit.as_view()),
    path('getHealthHistory/', getHealthHistory.as_view()),

]
