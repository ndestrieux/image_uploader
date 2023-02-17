from collections import OrderedDict

from rest_framework import serializers

from api.fields import BinaryField, ImageField, ThumbnailsField
from api.models import Image, Thumbnail


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
    image = ImageField(source="original")
    binary = BinaryField()
    thumbnails = ThumbnailsField(
        many=True, queryset=Thumbnail.objects.all(), slug_field="thumbnail"
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
