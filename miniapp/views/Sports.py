import datetime
from django.http import JsonResponse
from rest_framework.views import APIView
from miniapp.models import *
from miniapp.serializers import sportsRecordsSerializer, sportsTypeSerializer

# 运动记录
from miniapp.views.BloodSugarData import addIntegralHistory


class addSportsRecords(APIView):
    # authentication_classes = (authentication.JWTAuthentication,)

    authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId,is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        sportstypeid = request.data.get('sportstypeid')
        type = sportsType.objects.filter(id=sportstypeid).first()
        if not type:
            res['data'] = '类型不存在'
            res['status'] = 400
            return JsonResponse(res)
        startTime = request.data.get('startTime')
        endTime = request.data.get('endTime')
        startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
        endTime = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
        total_seconds = (endTime - startTime).total_seconds()
        mins = round(total_seconds / 60, 2)
        print(mins)
        heat = round(type.heat * mins, 2)
        status = 0
        sportTargetValueC = sportTargetValue.objects.filter(user=user).first()
        if sportTargetValueC:
            heatT = sportTargetValueC.heat
            if heatT < heat:
                IntegralDetailT = IntegralDetail.objects.filter(name="每日运动量达标").first()
                if IntegralDetailT:
                    user.integral += IntegralDetailT.integral
                    user.save()
                    addIntegralHistory(user, IntegralDetailT)
                status = 1
        sportsRecords.objects.create(user=user, startTime=startTime, endTime=endTime, sportstype=type, heat=heat,
                                     status=status)
        res['data'] = '记录成功'
        res['status'] = 200
        return JsonResponse(res)


class getSportsRecordsByid(APIView):
    # authentication_classes = (authentication.JWTAuthentication,)

    authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId,is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        list = sportsRecords.objects.filter(user=user).all().order_by('-time')
        if not list:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        res['data'] = sportsRecordsSerializer(list, many=True).data
        res['status'] = 200
        return JsonResponse(res)


class deleteSportsRecordsByid(APIView):
    # authentication_classes = (authentication.JWTAuthentication,)

    authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId,is_active=True).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        SportsRecordsId = request.data.get('SportsRecordsId')
        s = sportsRecords.objects.filter(id=SportsRecordsId).first()
        if not s:
            res['data'] = '记录不存在'
            res['status'] = 400
            return JsonResponse(res)
        s.delete()
        res['data'] = '已经删除'
        res['status'] = 200
        return JsonResponse(res)


class dailySportList(APIView):
    def get(self, request):
        res = {}
        data = []
        startdate = datetime.date(
            datetime.datetime.now().year,
            datetime.datetime.now().month,
            datetime.datetime.now().day)
        enddate = startdate + datetime.timedelta(days=1)
        list = sportsRecords.objects.filter(startTime__range=[startdate, enddate]).order_by('-heat')
        print(list)
        for item in list:
            data.append({
                'id': item.id,
                'user': {
                    'userid': item.user.id,
                    'username': item.user.username,
                    'avatar': item.user.avatar,
                    'gender': item.user.gender,
                },
                'sportstype': item.sportstype.name,
                'heat': item.heat,
                'startTime': item.startTime,
                # 'endTime': item.endTime,
            })
        res['data'] = data
        res['status'] = 200
        return JsonResponse(res)


class getsportsType(APIView):
    def get(self, request):
        res = {}
        list = sportsType.objects.all()
        res['data'] = sportsTypeSerializer(list, many=True).data
        res['status'] = 200
        return JsonResponse(res)
