from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework_simplejwt import authentication


class test(APIView):
    # authentication_classes = (authentication.JWTAuthentication,)
    authentication_classes = ()

    def get(self, request):
        res = {
            'code': 0,
            'msg': 'ok',
            'data': {
                'name': 'test'
            }
        }
        return JsonResponse(res)
