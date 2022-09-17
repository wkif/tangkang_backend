from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import tabList
from miniapp.serializers import tabListModelserializers, tabListCreateUpdateSerializer


class tabListModelViewset(CustomModelViewSet):
    queryset = tabList.objects.all()
    serializer_class = tabListModelserializers
    create_serializer_class = tabListCreateUpdateSerializer
    update_serializer_class = tabListCreateUpdateSerializer

    # queryset = miniappUser.objects.all()
    # serializer_class = miniappUserModelserializers
