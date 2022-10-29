from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from miniapp.models import *
from miniapp.serializers import foodDatabaseSerializer, dietRecordsSerializer

# 食品数据库--------------------------------------------------------start
from miniapp.views.BloodSugarData import addIntegralHistory


class getfoodDatabaseByname(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        foodName = request.data.get('foodName')
        foodData = foodDatabase.objects.filter(foodName__contains=foodName).all()
        print(foodData)
        if not foodData:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        data = [
            {
                'name': '全部',
                'food': foodDatabaseSerializer(foodData, many=True).data
            },
            {
                "name": "蔬菜",
                "food": []
            },
            {
                "name": "水果",
                "food": []
            },
            {
                "name": "肉类",

                "food": []
            },
            {
                "name": "蛋类",
                "food": []
            },
            {
                "name": "奶类",
                "food": []
            },
            {
                "name": "鱼类",
                "food": []
            },
            {
                "name": "豆类",
                "food": []
            },
            {
                "name": "谷物",
                "food": []
            },
            {
                "name": "其他",
                "food": []
            }

        ]
        for item in foodData:
            data[item.foodType + 1]['food'].append(foodDatabaseSerializer(item).data)

        res['data'] = {
            'foodDatabase': data
            , 'tablist': ['全部', '蔬菜', '水果', '肉类', '蛋类', '奶类', '鱼类', '豆类', '谷物', '其他']
        }
        res['status'] = 200
        return JsonResponse(res)


class getfoodDatabase(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request):
        res = {}
        foodDatabaseData = foodDatabase.objects.all()
        if not foodDatabaseData:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        res['data'] = foodDatabaseSerializer(foodDatabaseData, many=True).data
        res['status'] = 200

        return JsonResponse(res)


class getDietRecords(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        dietRecordsList = dietRecords.objects.filter(user=user).all().order_by('-time')
        if not dietRecordsList:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        res['data'] = dietRecordsSerializer(dietRecordsList, many=True).data
        res['status'] = 200
        return JsonResponse(res)


class addDietRecords(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        time = request.data.get('time')
        food = request.data.get('food')
        # foodCalory = request.data.get('foodCalory')
        foodProtein = request.data.get('foodProtein')
        foodFat = request.data.get('foodFat')
        foodCarbohydrate = request.data.get('foodCarbohydrate')
        foodVitaminA = request.data.get('foodVitaminA')
        foodVitaminC = request.data.get('foodVitaminC')
        foodVitaminE = request.data.get('foodVitaminE')
        foodVitaminD = request.data.get('foodVitaminD')
        heat = request.data.get('heat')

        di = dietRecords.objects.filter(user=user, time=time, food=food).first()
        if di:
            res['data'] = '该数据已经存在'
            res['status'] = 400
            return JsonResponse(res)
        status = 0
        dietTargetValueC = dietTargetValue.objects.filter(user=user).first()
        if dietTargetValueC:
            heatT = dietTargetValueC.heat
            if heat < heatT:
                IntegralDetailT = IntegralDetail.objects.filter(name="饮食热量达标").first()
                if IntegralDetailT:
                    user.integral += IntegralDetailT.integral
                    user.save()
                    addIntegralHistory(user, IntegralDetailT)
                status = 1
        dietRecords.objects.create(user=user, time=time, food=food, foodProtein=foodProtein,
                                   foodFat=foodFat, foodCarbohydrate=foodCarbohydrate, foodVitaminA=foodVitaminA,
                                   foodVitaminC=foodVitaminC, foodVitaminE=foodVitaminE, foodVitaminD=foodVitaminD,
                                   heat=heat, status=status)
        res['data'] = '添加成功'
        res['status'] = 200
        return JsonResponse(res)


class deleteDietRecords(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        dietId = request.data.get('dietId')
        diet = dietRecords.objects.filter(id=dietId).first()
        if not diet:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            diet.delete()
            res['data'] = '删除成功'
            res['status'] = 200
            return JsonResponse(res)

# 食品数据库--------------------------------------------------------end
