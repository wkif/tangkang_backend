from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from miniapp.models import *
from miniapp.serializers import announcementbaseserializer


# 公告--------------------------------------------------------start
class getNoticeData(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request):
        res = {}
        noticeData = announcement.objects.filter(release=True).all().order_by('-createTime')
        if not noticeData:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        res['data'] = announcementbaseserializer(noticeData, many=True).data
        res['status'] = 200
        return JsonResponse(res)


class getTopNoticeData(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request):
        res = {}
        noticeData = announcement.objects.filter(release=True).order_by('-createTime').first()
        if not noticeData:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        res['data'] = announcementbaseserializer(noticeData).data
        res['status'] = 200
        return JsonResponse(res)


# 公告--------------------------------------------------------end
