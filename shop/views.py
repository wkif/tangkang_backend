from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework_simplejwt import authentication

from shop.utils.upload_img import upload_img


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


class uploadImg(APIView):
    authentication_classes = ()

    def post(self, request):
        img = request.FILES.get('img')
        img_name = request.POST.get('imgName')
        ingUrl = upload_img(img, img_name)
        res = {
            'code': 0,
            'msg': 'ok',
            'data': {
                'imgUrl': ingUrl
            }
        }
        return JsonResponse(res)
