from random import choice
from string import ascii_uppercase as uc, digits as dg
import time
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from miniapp.models import *
from miniapp.serializers import userserializer, addressSerializer, JfwTokenObtainPairSerializer
from miniapp.utils.checkIdnum import check_id_data
from miniapp.utils.wxlogin import get_login_info


class loginApi(APIView):
    def post(self, request):
        res = {}
        code = request.data.get('code')
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
                token = JfwTokenObtainPairSerializer.get_token(a).access_token
                res['token'] = str(token)
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


class getUserIntegral(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            res['data'] = user.integral
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

        if not height or not weight or not birthday or not bloodType or not waistline:
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
