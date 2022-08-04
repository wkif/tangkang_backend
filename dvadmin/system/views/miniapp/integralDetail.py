from rest_framework.viewsets import ModelViewSet

from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import IntegralDetail
from miniapp.serializers import integralDetailModelserializers, integralDetailModelCreateUpdateSerializer


class integralDetailModelViewset(CustomModelViewSet):
    queryset = IntegralDetail.objects.all()
    serializer_class = integralDetailModelserializers
    create_serializer_class = integralDetailModelCreateUpdateSerializer
    update_serializer_class = integralDetailModelCreateUpdateSerializer

    # queryset = miniappUser.objects.all()
    # serializer_class = miniappUserModelserializers
