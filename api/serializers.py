from collections import OrderedDict
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from api.fields import BinaryImageField, OriginalImageField
from api.models import Image, Profile


class UploadImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="original")
    binary_expire_time = serializers.IntegerField(required=False)

    class Meta:
        model = Image
        fields = ["name", "image", "binary_expire_time"]

    def create(self, validated_data):
        uploaded_by = self.context["uploaded_by"]
        if validated_data.get("binary_expire_time", None):
            binary_expire_time = validated_data.pop("binary_expire_time")
            validated_data["binary_expiration_date"] = timezone.now() + timedelta(
                seconds=binary_expire_time
            )
        return Image.objects.create(uploaded_by=uploaded_by, **validated_data)

    def validate(self, attrs):
        user_profile = Profile.objects.get(user=self.context["uploaded_by"])
        if user_profile.binary_image_access and not attrs.get(
            "binary_expire_time", None
        ):
            raise serializers.ValidationError(
                {"binary_expire_time": "This field is required."}
            )
        return attrs

    def validate_binary_expire_time(self, value):
        user_profile = Profile.objects.get(user=self.context["uploaded_by"])
        if user_profile.binary_image_access:
            if 300 <= value <= 30000:
                return value
            raise serializers.ValidationError(
                "Binary image expire time should be between 300 and 30000 seconds."
            )
        raise serializers.ValidationError("This field is unexpected.")


class ImageListSerializer(serializers.ModelSerializer):
    image = OriginalImageField(source="original", view_name="image")
    binary = BinaryImageField(view_name="binary")
    thumbnails = serializers.HyperlinkedIdentityField(
        many=True, read_only=True, view_name="thumbnail"
    )

    class Meta:
        model = Image
        fields = [
            "name",
            "uploaded_on",
            "image",
            "binary",
            "thumbnails",
        ]

    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] is not None]
        )
