from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import announcement
from miniapp.serializers import announcementbaseModelserializers, announcementbaseModelCreateUpdateSerializer


class announcementbaseModelViewset(CustomModelViewSet):
    queryset = announcement.objects.all()
    serializer_class = announcementbaseModelserializers
    create_serializer_class = announcementbaseModelCreateUpdateSerializer
    update_serializer_class = announcementbaseModelCreateUpdateSerializer

