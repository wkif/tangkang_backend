from dvadmin.utils.viewset import CustomModelViewSet
from miniapp.models import userAgreement
from miniapp.serializers import userAgreementModelserializers, userAgreementModelCreateUpdateSerializer


class userAgreementModelViewset(CustomModelViewSet):
    queryset = userAgreement.objects.all()
    serializer_class = userAgreementModelserializers
    create_serializer_class = userAgreementModelCreateUpdateSerializer
    update_serializer_class = userAgreementModelCreateUpdateSerializer
