from rest_framework import serializers

from api.models import Profile


class OriginalImageField(serializers.HyperlinkedIdentityField):
    def get_attribute(self, instance):
        if Profile.objects.get(user=self.context["user"]).original_image_access:
            return super().get_attribute(instance)
        return None


class BinaryImageField(serializers.HyperlinkedIdentityField):
    def get_attribute(self, instance):
        if Profile.objects.get(user=self.context["user"]).binary_image_access:
            return super().get_attribute(instance)
        return None


class ThumbnailsField(serializers.SlugRelatedField):
    def to_representation(self, instance):
        url = instance.thumbnail.url
        request = self.context.get("request", None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url
