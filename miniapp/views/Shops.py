
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

from miniapp.models import *

from shop.models import SKU, OrderInfo, goodsCategory
from shop.serializers import SKUModelserializers, OrderInfoModelserializers

# 商店
class getShopList(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    # authentication_classes = ()

    def get(self, request):
        res = {}

        shopList = SKU.objects.filter(status=1)
        if not shopList:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            data = []
            categoryList = goodsCategory.objects.all()
            for category in categoryList:
                goods = SKU.objects.filter(category=category, status=1)
                data.append({
                    "id": category.id,
                    "name": category.name,
                    "goods": SKUModelserializers(goods, many=True).data
                })
            res['data'] = data
            res['status'] = 200
            return JsonResponse(res)


class getTopGoods(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    # authentication_classes = ()

    def get(self, request):
        res = {}
        goods = SKU.objects.filter(status=1, recommended=1)[:3]
        if not goods:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            res['data'] = SKUModelserializers(goods, many=True).data
            res['status'] = 200
            return JsonResponse(res)


class getGoodDetail(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    # authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        goodsId = request.data.get('goodsId')
        goods = SKU.objects.filter(id=goodsId, status=1).first()
        if not goods:
            res['data'] = '商品不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            data = SKUModelserializers(goods).data
            data['category'] = goodsCategory.objects.filter(id=data['category']).first().name
            res['data'] = data
            res['status'] = 200
            return JsonResponse(res)


class getGoodById(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    # authentication_classes = ()

    def post(self, request):
        res = {}
        goodsId = request.data.get('goodsId')
        goods = SKU.objects.filter(id=goodsId, status=1).first()
        if not goods:
            res['data'] = '商品不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            data = SKUModelserializers(goods).data
            res['data'] = data
            res['status'] = 200
            return JsonResponse(res)


class addOrder(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    # authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        addressId = request.data.get('addressId')
        addr = address.objects.filter(id=addressId).first()
        if not address:
            res['data'] = '地址不存在'
            res['status'] = 400
            return JsonResponse(res)
        goodId = request.data.get('goodId')
        good = SKU.objects.filter(id=goodId).first()
        if not good:
            res['data'] = '商品不存在'
            res['status'] = 400
            return JsonResponse(res)
        total_count = request.data.get('total_count')
        total_price = request.data.get('total_price')

        good.stock -= total_count
        good.sales += total_count
        good.save()
        ord = OrderInfo.objects.create(user=user, address=addr, good=good, total_count=total_count,
                                       total_price=total_price)
        res['data'] = '下单成功，请尽快付款'
        res['status'] = 200
        return JsonResponse(res)


class payment(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    # authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        orderId = request.data.get('orderId')
        order = OrderInfo.objects.filter(id=orderId).first()
        if not order:
            res['data'] = '订单不存在'
            res['status'] = 400
            return JsonResponse(res)
        if order.order_status == 6:
            res['data'] = '订单已取消'
            res['status'] = 400
            return JsonResponse(res)
        if order.order_status == 1:
            Amount_payable = order.total_price
            integral = user.integral
            if integral >= Amount_payable:
                user.integral = user.integral - Amount_payable
                user.save()
                order.order_status = 2
                order.save()
                integralHistory.objects.create(user=user, integral=Amount_payable,
                                               integralType=IntegralDetail.objects.filter(id=7).first())

                res['data'] = '支付成功'
                res['status'] = 200
                return JsonResponse(res)
            else:
                res['data'] = '积分不足'
                res['status'] = 400
                return JsonResponse(res)
        else:
            res['data'] = '订单已支付'
            res['status'] = 400
            return JsonResponse(res)


class cancelOrder(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    # authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        orderId = request.data.get('orderId')
        order = OrderInfo.objects.filter(id=orderId).first()
        if not order:
            res['data'] = '订单不存在'
            res['status'] = 400
            return JsonResponse(res)
        order.order_status = 6
        order.save()
        res['data'] = '取消成功'
        res['status'] = 200
        return JsonResponse(res)


class getMyOrderList(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    # authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        orderList = OrderInfo.objects.filter(user=user).order_by('-update_datetime')
        if not orderList:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            # data = {
            #     "1": OrderInfoModelserializers(
            #         OrderInfo.objects.filter(user=user, order_status=1).order_by('-update_datetime'), many=True).data,
            #     "2": OrderInfoModelserializers(
            #         OrderInfo.objects.filter(user=user, order_status=2).order_by('-update_datetime'), many=True).data,
            #     "3": OrderInfoModelserializers(
            #         OrderInfo.objects.filter(user=user, order_status=3).order_by('-update_datetime'), many=True).data,
            #     "4": OrderInfoModelserializers(
            #         OrderInfo.objects.filter(user=user, order_status=4).order_by('-update_datetime'), many=True).data,
            #     "5": OrderInfoModelserializers(
            #         OrderInfo.objects.filter(user=user, order_status=5).order_by('-update_datetime'), many=True).data,
            #     "6": OrderInfoModelserializers(
            #         OrderInfo.objects.filter(user=user, order_status=6).order_by('-update_datetime'), many=True).data,
            # }
            data = []
            data.append(OrderInfoModelserializers(
                OrderInfo.objects.filter(user=user, order_status=1).order_by('-update_datetime'), many=True).data, )
            data.append(OrderInfoModelserializers(
                OrderInfo.objects.filter(user=user, order_status=2).order_by('-update_datetime'), many=True).data, )
            data.append(OrderInfoModelserializers(

                OrderInfo.objects.filter(user=user, order_status=3).order_by('-update_datetime'), many=True).data, )
            data.append(OrderInfoModelserializers(
                OrderInfo.objects.filter(user=user, order_status=4).order_by('-update_datetime'), many=True).data, )
            data.append(OrderInfoModelserializers(
                OrderInfo.objects.filter(user=user, order_status=5).order_by('-update_datetime'), many=True).data, )
            data.append(OrderInfoModelserializers(
                OrderInfo.objects.filter(user=user, order_status=6).order_by('-update_datetime'), many=True).data, )

            res['data'] = data
            res['status'] = 200
            return JsonResponse(res)


class confirmOrder(APIView):
    authentication_classes = (authentication.JWTAuthentication,)

    # authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)

        orderId = request.data.get('orderId')
        order = OrderInfo.objects.filter(id=orderId).first()
        if not order:
            res['data'] = '订单不存在'
            res['status'] = 400
            return JsonResponse(res)
        if order.order_status == 3:
            order.order_status = 4
            order.save()
            res['data'] = '确认成功'
            res['status'] = 200
            return JsonResponse(res)
        else:
            res['data'] = '订单状态不正确'
            res['status'] = 400
            return JsonResponse(res)

