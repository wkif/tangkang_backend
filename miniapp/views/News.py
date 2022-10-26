import datetime
import re
from django.http import JsonResponse
from rest_framework.views import APIView
from miniapp.models import *
from miniapp.serializers import newsserializer, commitOfNewsserializer









# 资讯-------------------------------------------------
class getNewsList(APIView):
    # authentication_classes = (authentication.JWTAuthentication,)

    authentication_classes = ()

    def get(self, request):
        res = {}
        newsList = news.objects.all().order_by('-updateTime')
        if not newsList:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            for a in newsList:
                a.content = re.sub('<[^<]+?>', '', a.content).replace('\n', '').strip()
            data = newsserializer(newsList, many=True).data
            res['data'] = data
            res['status'] = 200
            return JsonResponse(res)


class getTopNews(APIView):
    # authentication_classes = (authentication.JWTAuthentication,)

    authentication_classes = ()

    def get(self, request):
        res = {}
        newsList = news.objects.filter(top=True, is_delete=False).order_by('-updateTime')
        if not newsList:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            data = []
            for n in newsList:
                data.append({
                    'id': n.id,
                    'title': n.title,
                    'url': n.cover,
                })
            res['data'] = data
            res['status'] = 200
            return JsonResponse(res)


class searchNews(APIView):
    def post(self, request):
        res = {}
        newsname = request.data.get('newsname')
        if not newsname:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)

        new = news.objects.filter(title__icontains=newsname, is_delete=False).all()
        if not new:
            res['data'] = '无数据'
            res['status'] = 400
            return JsonResponse(res)
        else:
            h = hotSearch.objects.filter(name=newsname).first()
            if h:
                h.count += 1
                h.save()
            else:
                hotSearch.objects.create(name=newsname, count=1)
            data = []
            for item in new:
                data.append({
                    'id': item.id,
                    'title': item.title
                })
            res['data'] = data
            res['status'] = 200
            return JsonResponse(res)


class getHotSearch(APIView):
    authentication_classes = ()

    def get(self, request):
        res = {}
        list = hotSearch.objects.all().order_by('count')[:5]
        data = []
        for item in list:
            data.append({
                'id': item.id,
                'name': item.name
            })
        res['data'] = data
        res['status'] = 200
        return JsonResponse(res)


class getNewsDetail(APIView):
    # authentication_classes = (authentication.JWTAuthentication,)

    authentication_classes = ()

    def post(self, request):
        res = {}
        newsId = request.data.get('newsId')
        new = news.objects.filter(id=newsId, is_delete=False).first()
        if not new:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            res['data'] = {
                'news': newsserializer(new).data,
            }
            res['status'] = 200
            return JsonResponse(res)


class getCommitOfNews(APIView):
    # authentication_classes = (authentication.JWTAuthentication,)

    authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        newsId = request.data.get('newsId')
        new = news.objects.filter(id=newsId).first()
        if not new:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        else:
            commitList = commitOfNews.objects.filter(news=new, is_delete=False).order_by('-time')
            res['data'] = commitOfNewsserializer(commitList, many=True).data
            res['status'] = 200
            return JsonResponse(res)


class addCommit(APIView):
    # authentication_classes = (authentication.JWTAuthentication,)

    authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        newsId = request.data.get('newsId')
        new = news.objects.filter(id=newsId, is_delete=False).first()
        if not new:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        content = request.data.get('content')
        hasC = commitOfNews.objects.filter(user=user, news=new).all().order_by('-time')
        if hasC:
            Time = hasC[0].time
            # 距离当前时间的时间间隔
            timeGap = (datetime.datetime.now() - Time).seconds
            if timeGap < 60:
                res['data'] = '评论过于频繁'
                res['status'] = 400
                return JsonResponse(res)

        commit = commitOfNews.objects.create(news=new, user=user, content=content)
        if not commit:
            res['data'] = '添加失败'
            res['status'] = 400
            return JsonResponse(res)
        else:
            res['data'] = '添加成功'
            res['status'] = 200
            return JsonResponse(res)


class deleteCommit(APIView):
    # authentication_classes = (authentication.JWTAuthentication,)

    authentication_classes = ()

    def post(self, request):
        res = {}
        userId = request.data.get('userId')
        user = miniappUser.objects.filter(id=userId).first()
        if not user:
            res['data'] = '用户不存在'
            res['status'] = 400
            return JsonResponse(res)
        newsId = request.data.get('newsId')
        new = news.objects.filter(id=newsId, is_delete=False).first()
        if not new:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        commitId = request.data.get('commitId')
        commit = commitOfNews.objects.filter(id=commitId, is_delete=False).first()
        if not commit:
            res['data'] = '数据不存在'
            res['status'] = 400
            return JsonResponse(res)
        if commit.user != user:
            res['data'] = '没有权限'
            res['status'] = 400
            return JsonResponse(res)
        else:
            commit.is_delete = True
            commit.save()
            res['data'] = '删除成功'
            res['status'] = 200
            return JsonResponse(res)
