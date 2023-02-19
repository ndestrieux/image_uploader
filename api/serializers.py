from collections import OrderedDict

from rest_framework import serializers

from api.fields import BinaryImageField, OriginalImageField
from api.models import Image


class UploadImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="original")
    binary_expire_time = serializers.IntegerField(required=False)

    class Meta:
        model = Image
        fields = ["name", "image", "binary_expire_time"]

    def create(self, validated_data):
        uploaded_by = self.context["uploaded_by"]
        return Image.objects.create(uploaded_by=uploaded_by, **validated_data)


class ImageListSerializer(serializers.ModelSerializer):
    image = OriginalImageField(source="original", view_name="image")
    binary = BinaryImageField(view_name="binary")
    thumbnails = serializers.HyperlinkedIdentityField(
        many=True, read_only=True, view_name="thumbnail"
    )

    class Meta:
        model = Image
        fields = [
            "image",
            "binary",
            "thumbnails",
        ]

    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] is not None]
        )
