from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import sportsType
from miniapp.serializers import sportsTypeModelserializers, sportsTypeCreateUpdateSerializer


class sportsTypeModelViewset(CustomModelViewSet):
    queryset = sportsType.objects.all()
    serializer_class = sportsTypeModelserializers
    create_serializer_class = sportsTypeCreateUpdateSerializer
    update_serializer_class = sportsTypeCreateUpdateSerializer

    # queryset = miniappUser.objects.all()
    # serializer_class = miniappUserModelserializers
