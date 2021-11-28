from rest_framework.serializers import ModelSerializer, StringRelatedField

from tires.models import TiresInfo


class TiresInfoCreateSerializer(ModelSerializer):
    class Meta:
        model = TiresInfo
        fields = (
            "username",
            "trim_id",
        )


class TireInfoReadSerializer(ModelSerializer):
    id = StringRelatedField(source="username")

    class Meta:
        model = TiresInfo
        fields = (
            "id",
            "trim_id",
            "front_width",
            "front_profile",
            "front_rim",
            "rear_width",
            "rear_profile",
            "rear_rim",
        )
