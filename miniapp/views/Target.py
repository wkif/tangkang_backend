from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from miniapp.models import *




# 血糖目标--------------------------------------------------------start

class addBloodGlucoseTargetValue(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)

        bloodSugar0_targetValue = request.data.get('bloodSugar0_targetValue')
        bloodSugar1_targetValue = request.data.get('bloodSugar1_targetValue')
        bloodSugar2_targetValue = request.data.get('bloodSugar2_targetValue')
        bloodSugar3_targetValue = request.data.get('bloodSugar3_targetValue')
        bloodSugar4_targetValue = request.data.get('bloodSugar4_targetValue')
        bloodSugar5_targetValue = request.data.get('bloodSugar5_targetValue')
        bloodSugar6_targetValue = request.data.get('bloodSugar6_targetValue')
        bloodSugar7_targetValue = request.data.get('bloodSugar7_targetValue')
        bloodSugar8_targetValue = request.data.get('bloodSugar8_targetValue')
        bloodSugar9_targetValue = request.data.get('bloodSugar9_targetValue')
        if not bloodSugar0_targetValue and not bloodSugar1_targetValue and not bloodSugar2_targetValue and not bloodSugar3_targetValue and not bloodSugar4_targetValue and not bloodSugar5_targetValue and not bloodSugar6_targetValue and not bloodSugar7_targetValue and not bloodSugar8_targetValue and not bloodSugar9_targetValue:
            res['data'] = '请输入目标值'
            res['status'] = 400
            return JsonResponse(res)
        targetValue = bloodGlucoseTargetValue.objects.filter(user=user).first()
        if targetValue:
            targetValue.bloodSugar0_targetValue = bloodSugar0_targetValue
            targetValue.bloodSugar1_targetValue = bloodSugar1_targetValue
            targetValue.bloodSugar2_targetValue = bloodSugar2_targetValue
            targetValue.bloodSugar3_targetValue = bloodSugar3_targetValue
            targetValue.bloodSugar4_targetValue = bloodSugar4_targetValue
            targetValue.bloodSugar5_targetValue = bloodSugar5_targetValue
            targetValue.bloodSugar6_targetValue = bloodSugar6_targetValue
            targetValue.bloodSugar7_targetValue = bloodSugar7_targetValue
            targetValue.bloodSugar8_targetValue = bloodSugar8_targetValue
            targetValue.bloodSugar9_targetValue = bloodSugar9_targetValue
            targetValue.save()
            res['data'] = '更新成功'
            res['status'] = 200
            return JsonResponse(res)
        else:
            bloodGlucoseTargetValue.objects.create(user=user, bloodSugar0_targetValue=bloodSugar0_targetValue,
                                                   bloodSugar1_targetValue=bloodSugar1_targetValue,
                                                   bloodSugar2_targetValue=bloodSugar2_targetValue,
                                                   bloodSugar3_targetValue=bloodSugar3_targetValue,
                                                   bloodSugar4_targetValue=bloodSugar4_targetValue,
                                                   bloodSugar5_targetValue=bloodSugar5_targetValue,
                                                   bloodSugar6_targetValue=bloodSugar6_targetValue,
                                                   bloodSugar7_targetValue=bloodSugar7_targetValue,
                                                   bloodSugar8_targetValue=bloodSugar8_targetValue,
                                                   bloodSugar9_targetValue=bloodSugar9_targetValue)
            res['data'] = '添加成功'
            res['status'] = 200
            return JsonResponse(res)


class getBloodGlucoseTargetValue(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        targetValue = bloodGlucoseTargetValue.objects.filter(user=user).first()
        if not targetValue:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            res['data'] = {
                'targetValue': {
                    'bloodSugar0_targetValue': targetValue.bloodSugar0_targetValue,
                    'bloodSugar1_targetValue': targetValue.bloodSugar1_targetValue,
                    'bloodSugar2_targetValue': targetValue.bloodSugar2_targetValue,
                    'bloodSugar3_targetValue': targetValue.bloodSugar3_targetValue,
                    'bloodSugar4_targetValue': targetValue.bloodSugar4_targetValue,
                    'bloodSugar5_targetValue': targetValue.bloodSugar5_targetValue,
                    'bloodSugar6_targetValue': targetValue.bloodSugar6_targetValue,
                    'bloodSugar7_targetValue': targetValue.bloodSugar7_targetValue,
                    'bloodSugar8_targetValue': targetValue.bloodSugar8_targetValue,
                    'bloodSugar9_targetValue': targetValue.bloodSugar9_targetValue,
                },
                'createTime': targetValue.createDate.strftime('%Y-%m-%d %H:%M:%S'),
                'updateTime': targetValue.updateDate.strftime('%Y-%m-%d %H:%M:%S'),
            }
            res['status'] = 200
            return JsonResponse(res)