from django.http import HttpResponseGone, HttpResponseNotFound
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

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
            return HttpResponseNotFound("Image not available")
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
        if instance.binary_expiration_date < timezone.now():
            return HttpResponseGone("The link has expired")
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
