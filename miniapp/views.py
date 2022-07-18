import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from miniapp.models import miniappUser
from miniapp.serializers import userserializer
from miniapp.utils.creatToken import creattoken
from miniapp.utils.wxlogin import get_login_info


class loginApi(APIView):
    def post(self, request):
        res = {}
        print(request)
        # 微信登录
        code = request.data.get('code')
        print(code)
        user_data = get_login_info(code)
        info = request.data.get('info')
        if user_data:
            u = miniappUser.objects.filter(openid=user_data['openid'], is_active=True).first()
            if not u:
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                miniappUser.objects.create(openid=user_data['openid'], name=info['nickName'],
                                           avatar=info['avatarUrl'], userRegDate=create_time)
            miniappUser.objects.update()
            e = miniappUser.objects.filter(openid=user_data['openid'], is_active=True).first()
            if e.phone == '':
                res['getphone'] = False
            else:
                res['getphone'] = True
            re = userserializer(e)
            res['queryResult'] = re.data
            res['status'] = 200
            token = creattoken(user_data)
            print(token)
            res['token'] = token
            return JsonResponse(res)
        else:
            return JsonResponse({'status': 400, 'message': "未获取到openid，联系开发人员"})
