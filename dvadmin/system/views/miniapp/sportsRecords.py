from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import sportsRecords
from miniapp.serializers import sportsRecordsModelserializers, sportsRecordsCreateUpdateSerializer


class sportsRecordsModelViewset(CustomModelViewSet):
    queryset = sportsRecords.objects.all()
    serializer_class = sportsRecordsModelserializers
    create_serializer_class = sportsRecordsCreateUpdateSerializer
    update_serializer_class = sportsRecordsCreateUpdateSerializer

    # queryset = miniappUser.objects.all()
    # serializer_class = miniappUserModelserializers
