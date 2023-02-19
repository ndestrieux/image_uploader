from datetime import datetime as dt
from datetime import timedelta

import pytz
from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.models import Image, Profile, Thumbnail
from api.renderers import JPEGRenderer, PNGRenderer
from api.serializers import ImageListSerializer, UploadImageSerializer


class UploadImageView(CreateAPIView):
    serializer_class = UploadImageSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = Profile.objects.get(user=self.get_user())
        if (
            serializer.validated_data.get("binary_expire_time", None)
            and user_profile.binary_image_access
        ):
            binary_expire_time = serializer.validated_data.pop(
                "binary_expire_time", None
            )
            serializer.validated_data["binary_expiration_date"] = dt.now() + timedelta(
                seconds=binary_expire_time
            )
        elif user_profile.binary_image_access:
            raise ValidationError("binary_expire_time field expected.")
        elif serializer.validated_data.get("binary_expire_time", None):
            raise ValidationError("binary_expire_time field unexpected.")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            "success": f"Image '{serializer.data['name']}' has been uploaded successfully!"
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uploaded_by"] = self.get_user()
        return context

    def get_user(self):
        key = self.request.META.get("HTTP_AUTHORIZATION").split()[-1]
        return Token.objects.get(key=key).user


class ImageListAPIView(ListAPIView):
    serializer_class = ImageListSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.get_user()
        return context

    def get_queryset(self):
        return Image.objects.filter(uploaded_by=self.get_user())

    def get_user(self):
        key = self.request.META.get("HTTP_AUTHORIZATION").split()[-1]
        return Token.objects.get(key=key).user


class OriginalImageView(RetrieveAPIView):
    renderer_classes = (
        PNGRenderer,
        JPEGRenderer,
    )
    queryset = Image.objects.all()
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        uploader_profile = Profile.objects.get(user=instance.uploaded_by)
        if not uploader_profile.original_image_access:
            raise Http404
        data = instance.original
        return Response(data)


class BinaryImageView(RetrieveAPIView):
    renderer_classes = (
        PNGRenderer,
        JPEGRenderer,
    )
    queryset = Image.objects.all()
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.binary_expiration_date.replace(tzinfo=pytz.utc) < dt.now().replace(
            tzinfo=pytz.utc
        ):
            raise Http404
        data = instance.binary
        return Response(data)


class ThumbnailView(RetrieveAPIView):
    renderer_classes = (
        PNGRenderer,
        JPEGRenderer,
    )
    queryset = Thumbnail.objects.all()
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = instance.thumbnail
        return Response(data)
