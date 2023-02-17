from rest_framework import serializers

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
