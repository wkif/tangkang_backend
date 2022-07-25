from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import foodDatabase
from miniapp.serializers import foodDatabaseModelserializers, foodDatabaseModelCreateUpdateSerializer


class foodDatabaseModelViewset(CustomModelViewSet):
    queryset = foodDatabase.objects.all()
    serializer_class = foodDatabaseModelserializers
    create_serializer_class = foodDatabaseModelCreateUpdateSerializer
    update_serializer_class = foodDatabaseModelCreateUpdateSerializer

    # queryset = miniappUser.objects.all()
    # serializer_class = miniappUserModelserializers
