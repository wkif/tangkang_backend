from django.http import JsonResponse
from rest_framework.views import APIView
from miniapp.models import *


class getUserAgreement(APIView):
    # authentication_classes = ()  # 在此重新定义认证方式
    # permission_classes = ()  # 在此重新定义权限

    def get(self, request):
        res = {}
        UserAgreement = userAgreement.objects.all().order_by('-id')
        if UserAgreement:
            content = UserAgreement.first().content
            res['data'] = {
                'content': content,
                'createTime': UserAgreement.first().createTime,
                'updateTime': UserAgreement.first().updateTime

            }

        else:
            res['data'] = '暂无内容'
        res['status'] = 200
        return JsonResponse(res)


class getTabList(APIView):
    def get(self, request):
        res = {}
        tablist = tabList.objects.filter(is_active=True).all()
        list = []
        for item in tablist:
            list.append({
                'name': item.name,
                'selectedIconPath': item.selectedIconPath,
                'iconPath': item.iconPath,
                'pagePath': item.pagePath.path
            })
        res['data'] = list
        res['status'] = 200
        return JsonResponse(res)


class changespeed(APIView):
    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            if user.speed:
                user.speed = False
            else:
                user.speed = True
            user.save()
            res['data'] = '修改成功'
            res['status'] = 200
            return JsonResponse(res)


class getSpeed(APIView):
    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            if user.speed:
                res['data'] = 1
                res['status'] = 200
                return JsonResponse(res)
            else:
                res['data'] = 0
                res['status'] = 200
                return JsonResponse(res)
