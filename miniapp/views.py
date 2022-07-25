from random import choice
from string import ascii_uppercase as uc, digits as dg
import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.tokens import RefreshToken

from dvadmin.utils.permission import CustomPermission
from miniapp.extensions.auth import JwtQueryParamsAuthentication
from miniapp.models import *
from miniapp.serializers import userserializer, addressSerializer, JfwTokenObtainPairSerializer, bloodSugarSerializer, \
    periodicalLoggingSerializer, announcementbaseserializer, foodDatabaseSerializer
from miniapp.utils.checkIdnum import check_id_data
from miniapp.utils.creatToken import creattoken
from miniapp.utils.wxlogin import get_login_info
from rest_framework_simplejwt.views import TokenObtainPairView


class loginApi(APIView):
    def post(self, request):
        res = {}
        # print(request)
        # 微信登录
        code = request.data.get('code')
        # print(code)
        user_data = get_login_info(code)
        info = request.data.get('info')
        inviteCode = request.data.get('inviteCode')

        if user_data:
            u = miniappUser.objects.filter(openid=user_data['openid']).first()
            if not u:
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                part1 = ''.join(choice(uc) for j in range(3))  # 三个大写的英文
                part2 = ''.join(choice(dg) for j in range(3))  # 三个随机数字
                part3 = ''.join(choice(dg + uc) for j in range(10))  # 十个随机大写字母或者数字
                singleMark = part1 + part2 + part3
                a = miniappUser.objects.create(openid=user_data['openid'], username=info['nickName'],
                                               avatar=info['avatarUrl'], userRegDate=create_time, gender=info['gender'],
                                               inviteCode=singleMark)
                if inviteCode:
                    u1 = miniappUser.objects.filter(inviteCode=inviteCode, is_active=True).first()
                    if u1:
                        u1.numberofPersonsInvited += 1
                miniappUser.objects.update()
                re = userserializer(a)
                res['data'] = re.data
                res['status'] = 200
                # token = creattoken(user_data)
                token = JfwTokenObtainPairSerializer.get_token(a).access_token
                # print((token))
                res['token'] = str(token)
                # print(res)
                return JsonResponse(res)
            else:
                if u.is_active:
                    re = userserializer(u)
                    res['data'] = re.data
                    res['status'] = 200
                    # token = creattoken(user_data)
                    token = JfwTokenObtainPairSerializer.get_token(u).access_token
                    # print((token))
                    res['token'] = str(token)
                    # print(res)
                    return JsonResponse(res)
                else:
                    res['status'] = 400
                    res['msg'] = '该账号已被禁用'
                    return JsonResponse(res)
        else:
            return JsonResponse({'status': 400, 'message': "未获取到openid，联系开发人员"})


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


class getAddressByUsrid(GenericAPIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        addList = address.objects.filter(user=user).all()
        if not addList:
            res['data'] = '暂无地址'
            res['status'] = 400
            return JsonResponse(res)
        else:
            res['data'] = addressSerializer(addList, many=True).data
            res['status'] = 200
            return JsonResponse(res)


class addAddressByUserid(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        name = request.data.get('name')
        phone = request.data.get('phone')
        addr = request.data.get('address')
        postalCode = request.data.get('postalCode')
        isDefault = request.data.get('isDefault')
        baseAddress = request.data.get('baseAddress')
        if not name or not phone or not addr or not baseAddress:
            res['data'] = '请填写完整信息'
            res['status'] = 400
            return JsonResponse(res)
        addressList = address.objects.filter(user=user).all()
        if addressList:
            for i in addressList:
                if i.name == name and i.phone == phone and i.address == addr and i.postalCode == postalCode and i.baseAddress == baseAddress:
                    res['data'] = '该地址已存在'
                    res['status'] = 400
                    return JsonResponse(res)
            if isDefault:
                for i in addressList:
                    i.isDefault = False
                    i.save()
        else:
            isDefault = True
        add = address.objects.create(user=user, name=name, phone=phone, address=addr, postalCode=postalCode,
                                     isDefault=isDefault, baseAddress=baseAddress)
        if add:
            res['status'] = 200
            res['data'] = '添加成功'
            res['status'] = 200
            return JsonResponse(res)
        else:
            res['data'] = '添加失败'
            res['status'] = 400
            return JsonResponse(res)


class editAddress(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        addressId = request.data.get('addressId')
        add = address.objects.filter(id=addressId).first()
        if not add:
            res['data'] = '地址不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            name = request.data.get('name')
            phone = request.data.get('phone')
            addr = request.data.get('address')
            postalCode = request.data.get('postalCode')
            isDefault = request.data.get('isDefault')
            baseAddress = request.data.get('baseAddress')
            add.name = name
            add.phone = phone
            add.addr = addr
            add.postalCode = postalCode
            add.baseAddress = baseAddress
            if not isDefault:
                if add.isDefault:
                    aList = address.objects.all()
                    for i in aList:
                        if i != add:
                            i.isDefault = True
                            i.save()
                            break
                    add.isDefault = False
                    add.save()
            else:
                if not add.isDefault:
                    aList = address.objects.all()
                    for i in aList:
                        if i.isDefault:
                            i.isDefault = False
                            i.save()
                    add.isDefault = True
            add.save()
            res['data'] = '修改成功'
            res['status'] = 200
            return JsonResponse(res)


class deleteAddressByUserid(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        addressId = request.data.get('addressId')
        add = address.objects.filter(id=addressId).first()
        if not add:
            res['data'] = '地址不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            if add.isDefault:
                add.delete()
                addF = address.objects.first()
                if addF:
                    addF.isDefault = True
                    addF.save()
            else:
                add.delete()
            res['data'] = '删除成功'
            res['status'] = 200
            return JsonResponse(res)


class editUserInfo(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        email = request.data.get('email')
        gender = request.data.get('gender')
        height = request.data.get('height')
        weight = request.data.get('weight')
        birthday = request.data.get('birthday')
        bloodType = request.data.get('bloodType')
        waistline = request.data.get('waistline')
        mobile = request.data.get('mobile')

        if not gender or not height or not weight or not birthday or not bloodType or not waistline:
            res['data'] = '请填写完整信息'
            res['status'] = 400
            return JsonResponse(res)
        user.email = email
        user.gender = gender
        user.height = height
        user.weight = weight
        user.birthday = birthday
        user.bloodType = bloodType
        user.waistline = waistline
        user.mobile = mobile
        user.save()
        res['data'] = '修改成功'
        res['status'] = 200
        return JsonResponse(res)


class getUserInfoByUserId(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        res['data'] = userserializer(user).data
        res['status'] = 200
        return JsonResponse(res)


class realnameAuthentication(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        realName = request.data.get('realName')
        idCard = request.data.get('idCard')
        flag = check_id_data(idCard)

        if not realName or not idCard:
            res['data'] = '请填写完整信息'
            res['status'] = 400
            return JsonResponse(res)
        if not flag:
            res['data'] = '身份证号码错误'
            res['status'] = 400
            return JsonResponse(res)
        user.realName = realName
        user.ID_number = idCard
        user.realNameAuthentication = True
        user.save()
        res['data'] = '修改成功'
        res['status'] = 200
        return JsonResponse(res)


# 血糖记录--------------------------------------------------------start

class getBloodSugarDataByUserId(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        bloodSugarData = bloodSugarLevels.objects.filter(user=user).all().order_by('bloodSugarTime')
        if not bloodSugarData:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        res['data'] = bloodSugarSerializer(bloodSugarData, many=True).data
        res['status'] = 200
        return JsonResponse(res)


class getLastBloodSugarDataByUserId(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
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
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        bloodSugarLevel = request.data.get('bloodSugarLevel')
        bloodSugarTime = request.data.get('bloodSugarTime')
        bloodSugarType = request.data.get('bloodSugarType')
        if not bloodSugarLevel or not bloodSugarTime or not bloodSugarType:
            res['data'] = '请填写完整信息'
            res['status'] = 400
            return JsonResponse(res)
        bloodSugarLevels.objects.create(user=user, bloodSugarLevel=bloodSugarLevel, bloodSugarTime=bloodSugarTime,
                                        bloodSugarType=bloodSugarType)
        res['data'] = '添加成功'
        res['status'] = 200
        return JsonResponse(res)


class deleteBloodSugarData(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
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

# 定期记录--------------------------------------------------------start

class getperiodicalLoggingDataByUserId(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        periodicalLoggingData = periodicalLogging.objects.filter(user=user).all().order_by('periodicalTime')
        if not periodicalLoggingData:
            res['data'] = '暂无数据'
            res['status'] = 400
            return JsonResponse(res)
        res['data'] = periodicalLoggingSerializer(periodicalLoggingData, many=True).data
        res['status'] = 200
        return JsonResponse(res)


class addPeriodicalLoggingData(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        periodicalTime = request.data.get('periodicalTime')
        glycosylatedHemoglobin = request.data.get('glycosylatedHemoglobin')
        microalbuminuria = request.data.get('microalbuminuria')
        dorsalisPedisArtery = request.data.get('dorsalisPedisArtery')
        if not periodicalTime or not glycosylatedHemoglobin or not microalbuminuria or not dorsalisPedisArtery:
            res['data'] = '请填写完整信息'
            res['status'] = 400
            return JsonResponse(res)
        periodicalLogging.objects.create(user=user, periodicalTime=periodicalTime,
                                         glycosylatedHemoglobin=glycosylatedHemoglobin,
                                         microalbuminuria=microalbuminuria, dorsalisPedisArtery=dorsalisPedisArtery)
        res['data'] = '添加成功'
        res['status'] = 200
        return JsonResponse(res)


class deletePeriodicalLoggingData(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        periodicalLoggingId = request.data.get('periodicalLoggingId')
        periodicalLogg = periodicalLogging.objects.filter(id=periodicalLoggingId).first()
        if not periodicalLogg:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        periodicalLogg.delete()
        res['data'] = '删除成功'
        res['status'] = 200
        return JsonResponse(res)


# 定期记录--------------------------------------------------------end

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


# 食品数据库--------------------------------------------------------start
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
# 食品数据库--------------------------------------------------------end
