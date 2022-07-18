from rest_framework import serializers

from dvadmin.utils.serializers import CustomModelSerializer
from miniapp.models import miniappUser, foodDatabase


class miniappUserModelserializers(CustomModelSerializer):
    class Meta:
        model = miniappUser
        exclude = ["password"]


class miniappUserModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = miniappUser
        fields = '__all__'


class userserializer(serializers.ModelSerializer):
    class Meta:
        model = miniappUser
        exclude = ["password", "is_active"]
        # fields = '__all__'



class foodDatabaseModelserializers(CustomModelSerializer):
    class Meta:
        model = foodDatabase



class foodDatabaseModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = foodDatabase
        fields = '__all__'


class foodDatabaseserializer(serializers.ModelSerializer):
    class Meta:
        model = foodDatabase
        fields = '__all__'