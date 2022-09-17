from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import news
from miniapp.serializers import newsModelserializers, newsModelCreateUpdateSerializer


class newsModelViewset(CustomModelViewSet):
    queryset = news.objects.all()
    serializer_class = newsModelserializers
    create_serializer_class = newsModelCreateUpdateSerializer
    update_serializer_class = newsModelCreateUpdateSerializer

    # queryset = miniappUser.objects.all()
    # serializer_class = miniappUserModelserializers
