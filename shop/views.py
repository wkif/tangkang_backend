from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework_simplejwt import authentication

from miniapp.models import miniappUser
from shop.models import goodsCategory, Brand, SKUCommits, SKU
from shop.utils.upload_file import upload_file


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
        ingUrl = upload_file(img, img_name)
        res = {
            'code': 0,
            'msg': 'ok',
            'data': {
                'imgUrl': ingUrl
            }
        }
        return JsonResponse(res)


class getSKUcategory(APIView):
    authentication_classes = ()

    def get(self, request):
        goodsCategoryList = goodsCategory.objects.all()
        data = []
        for i in goodsCategoryList:
            obj = {
                'label': i.name,
                'value': i.id
            }
            data.append(obj)
        res = {
            'status': 200,
            'msg': 'ok',
            'data': data
        }

        return JsonResponse(res)


class getSKUBrand(APIView):
    authentication_classes = ()

    def get(self, request):
        goodsBrandList = Brand.objects.all()
        data = []
        for i in goodsBrandList:
            obj = {
                'label': i.name,
                'value': i.id
            }
            data.append(obj)
        res = {
            'status': 200,
            'msg': 'ok',
            'data': data
        }

        return JsonResponse(res)


class deleteCommitById(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request):
        id = request.GET.get('id')
        c = SKUCommits.objects.get(id=id)
        if not c:
            res = {
                'status': 400,
                'msg': '评论不存在'
            }
            return JsonResponse(res)
        c.is_delete = True
        c.save()
        res = {
            'status': 200,
            'msg': 'ok',
        }
        return JsonResponse(res)

