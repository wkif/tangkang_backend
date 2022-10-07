
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

from miniapp.models import *
from miniapp.serializers import  integralHistorySerializer






class getIntegralHistory(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        integralHistoryData = integralHistory.objects.filter(user=user).order_by('-time')
        if not integralHistoryData:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            res['data'] = res['data'] = integralHistorySerializer(integralHistoryData, many=True).data
            res['status'] = 200
            return JsonResponse(res)
