import datetime
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from miniapp.models import *
from miniapp.serializers import bloodSugarSerializer


# 血糖记录--------------------------------------------------------start

def addIntegralHistory(user, integralType):
    integralHistory.objects.create(user=user, integralType=integralType)


class getBloodSugarDataByUserId(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId, is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        dateType = request.data.get('dateType')

        data = {}
        days = 0
        if dateType == '0' or dateType == 0:
            days = 7
        elif dateType == '1' or dateType == 1:
            days = 30

        date = datetime.datetime.now().date()
        date_r = date - datetime.timedelta(days=days)

        bloodSugarData = bloodSugarLevels.objects.filter(user=user, bloodSugarTime__range=(
            date_r, datetime.datetime.now().date() + datetime.timedelta(days=1))).order_by(
            '-bloodSugarTime')
        series = [
            {
                'name': '',
                'data': [None for x in range(days)]
            }
            for i in range(10)
        ]
        xAxisData = []
        for i in bloodSugarData:
            for d in range(days):
                # if i.bloodSugarTime.strftime('%m-%d') not in xAxisData:
                #     xAxisData.append(i.bloodSugarTime.strftime('%m-%d'))
                ds = date - datetime.timedelta(days=d)
                if ds not in xAxisData:
                    xAxisData.append(ds)
                if i.bloodSugarTime.date() == ds:
                    series[i.bloodSugarType]['data'][d] = i.bloodSugarLevel
                    # break

        legendData = ['空腹血糖', '早餐后2小时血糖', '午餐前血糖', '午餐后2小时血糖', '晚餐前血糖', '晚餐后2小时血糖', '睡前血糖', '任意时间血糖', '夜间2时血糖', '其他']
        for i in range(len(legendData)):
            series[i]['name'] = legendData[i]
        data['series'] = series
        data['xAxisData'] = xAxisData
        data['legendData'] = legendData

        if not data:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        else:
            res['data'] = {
                'chartsData': data,
                'cardData': bloodSugarSerializer(bloodSugarData, many=True).data
            }
            res['status'] = 200
            return JsonResponse(res)


class getLastBloodSugarDataByUserId(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId, is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        bloodSugarData = bloodSugarLevels.objects.filter(user=user).all().order_by('-bloodSugarTime').first()
        if not bloodSugarData:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        res['data'] = bloodSugarSerializer(bloodSugarData).data
        res['status'] = 200
        return JsonResponse(res)


class addBloodSugarData(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId, is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        bloodSugarLevel = request.data.get('bloodSugarLevel')
        bloodSugarTime = request.data.get('bloodSugarTime')
        bloodSugarType = request.data.get('bloodSugarType')
        if not bloodSugarLevel or not bloodSugarTime:
            res['data'] = '请填写完整信息'
            res['status'] = 400
            return JsonResponse(res)
        today = bloodSugarTime.split(' ')[0]
        nextday = (datetime.datetime.strptime(today, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        hasHis = bloodSugarLevels.objects.filter(user=user, bloodSugarTime__range=(today, nextday),
                                                 bloodSugarType=bloodSugarType).first()
        if hasHis:
            res['data'] = '该日期已存在数据'
            res['status'] = 400
            return JsonResponse(res)
        else:
            targetValueData = bloodGlucoseTargetValue.objects.filter(user=user).first()
            if not targetValueData:
                status = 1
            else:
                key = 'bloodSugar' + str(bloodSugarType) + '_targetValue'
                targetVlaue = (targetValueData.__dict__[key])
                print(targetVlaue)
                # eval
                if (float(bloodSugarLevel)) < float(targetVlaue[0]) or (float(bloodSugarLevel)) > float(
                        targetVlaue[1]):
                    status = 0
                else:
                    status = 1
                    tarObj = IntegralDetail.objects.filter(name='血糖值日记录达标').first()
                    if tarObj:
                        user.integral += tarObj.integral
                        user.save()
                        addIntegralHistory(user, tarObj)
                    else:
                        res['data'] = '联系客服设置积分值'
                        res['status'] = 400
                        return JsonResponse(res)
            bloodSugarLevels.objects.create(user=user, bloodSugarLevel=bloodSugarLevel, bloodSugarTime=bloodSugarTime,
                                            bloodSugarType=bloodSugarType, status=status)
            res['data'] = '添加成功'
            res['status'] = 200
            return JsonResponse(res)


class deleteBloodSugarData(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId, is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        bloodSugarId = request.data.get('bloodSugarId')
        bloodSugar = bloodSugarLevels.objects.filter(id=bloodSugarId).first()
        if not bloodSugar:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        bloodSugar.delete()
        res['data'] = '删除成功'
        res['status'] = 200
        return JsonResponse(res)

# 血糖记录--------------------------------------------------------end
