from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework_simplejwt import authentication

from dvadmin.utils.viewset import CustomModelViewSet
from shop.models import *
from shop.serializers import *


class commodityDlassificationData(APIView):
    authentication_classes = ()

    def get(self, request):
        data = []
        commodityDlassification = SKU.objects.all()
        for i in commodityDlassification:
            if data:
                for da in data:
                    if da['name'] == i.category.name:
                        da['value'] += 1
                        break
                    else:
                        obj = {
                            'name': i.category.name,
                            'value': 1
                        }
                        data.append(obj)
                        break
            else:
                obj = {
                    'name': i.category.name,
                    'value': 1
                }
                data.append(obj)

        return JsonResponse({"data": data})


class getDailyOrder(APIView):
    authentication_classes = ()

    def get(self, request):
        data = {
            'xAxis': [],
            'series': []
        }
        orderList = OrderInfo.objects.all()
        for i in orderList:
            dayTime = i.update_datetime.strftime('%Y-%m-%d')
            if dayTime in data['xAxis']:
                index = data['xAxis'].index(dayTime)
                data['series'][index] += 1
            else:
                data['xAxis'].append(dayTime)
                data['series'].append(1)
        res = {
            'data': data,
            'status': 200
        }
        return JsonResponse(res)


class getBrandData(APIView):
    authentication_classes = ()

    def get(self, request):
        data = []
        getBrandData = SKU.objects.all()
        for i in getBrandData:
            if data:
                for da in data:
                    if da['name'] == i.brand.name:
                        da['value'] += 1
                        break
                    else:
                        obj = {
                            'name': i.brand.name,
                            'value': 1
                        }
                        data.append(obj)
                        break
            else:
                obj = {
                    'name': i.brand.name,
                    'value': 1
                }
                data.append(obj)

        return JsonResponse({"data": data})


class SKUModelViewset(CustomModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUModelserializers
    create_serializer_class = SKUModelCreateUpdateSerializer
    update_serializer_class = SKUModelCreateUpdateSerializer


class SKUCategoryModelViewset(CustomModelViewSet):
    queryset = goodsCategory.objects.all()
    serializer_class = goodsCategoryModelserializers
    create_serializer_class = goodsCategoryModelCreateUpdateSerializer
    update_serializer_class = goodsCategoryModelCreateUpdateSerializer


class SKUBrandModelViewset(CustomModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandModelserializers
    create_serializer_class = BrandModelCreateUpdateSerializer
    update_serializer_class = BrandModelCreateUpdateSerializer


class OrderInfoModelViewset(CustomModelViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderInfoModelserializers
    create_serializer_class = OrderInfoModelCreateSerializer
    update_serializer_class = OrderInfoModelUpdateSerializer

# class getOrderLidt(APIView):
#     authentication_classes = (authentication.JWTAuthentication,)
#
#     def get(self, request):
#         list = OrderInfo.objects.all()
#         if not list:
#             return JsonResponse({"data": "暂无数据",
#                                  "status": 400})
#         else:
#             res = {
#                 'data': OrderInfoModelserializers(list, many=True).data,
#                 'status': 200,
#                 'msg': 'success'
#             }
#             return JsonResponse(res)
#
#
# class editOrder(APIView):
#     authentication_classes = ()
#
#     def post(self, request):
#         res = {}
#         orderId = request.data.get('orderId')
#         transit_price = request.data.get('transit_price')
#         order_status = request.data.get('order_status')
#         tracking_number = request.data.get('tracking_number')
#         order = OrderInfo.objects.filter(id=orderId).first()
#         if not order:
#             return JsonResponse({"data": "暂无数据",
#                                  "status": 400})
#         else:
#             order.transit_price = transit_price
#             order.order_status = order_status
#             order.tracking_number = tracking_number
#             order.save()
#             return JsonResponse(res)
