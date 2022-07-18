from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import miniappUser
from miniapp.serializers import miniappUserModelserializers, miniappUserModelCreateUpdateSerializer


class miniappUserModelViewset(CustomModelViewSet):
    queryset = miniappUser.objects.all()
    serializer_class = miniappUserModelserializers
    create_serializer_class = miniappUserModelCreateUpdateSerializer
    update_serializer_class = miniappUserModelCreateUpdateSerializer
    filter_fields = ['gender', 'is_active']
    search_fields = ['username']
    # queryset = miniappUser.objects.all()
    # serializer_class = miniappUserModelserializers
