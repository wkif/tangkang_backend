from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import commitOfNews
from miniapp.serializers import commitOfNewsModelCreateUpdateSerializer, commitOfNewsModelserializers


class commitOfNewsModelViewset(CustomModelViewSet):
    queryset = commitOfNews.objects.all()
    serializer_class = commitOfNewsModelserializers
    create_serializer_class = commitOfNewsModelCreateUpdateSerializer
    update_serializer_class = commitOfNewsModelCreateUpdateSerializer

    # queryset = miniappUser.objects.all()
    # serializer_class = miniappUserModelserializers
