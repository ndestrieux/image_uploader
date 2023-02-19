from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


from rest_framework.serializers import ValidationError
from datetime import datetime as dt, timedelta

from api.models import Image
from api.serializers import ImageListSerializer, UploadImageSerializer


class UploadImageView(CreateAPIView):
    serializer_class = UploadImageSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = Profile.objects.get(user=self.get_user())
        if serializer.validated_data.get("binary_expire_time", None) and user_profile.binary_image_access:
            binary_expire_time = serializer.validated_data.pop("binary_expire_time", None)
            serializer.validated_data["binary_expiration_date"] = dt.now() + timedelta(seconds=binary_expire_time)
        elif user_profile.binary_image_access:
            raise ValidationError("binary_expire_time field expected.")
        else:
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
    renderer_classes = (JSONRenderer, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.get_user()
        return context

    def get_queryset(self):
        return Image.objects.filter(uploaded_by=self.get_authorized_user())

    def get_user(self):
        key = self.request.META.get("HTTP_AUTHORIZATION").split()[-1]
        return Token.objects.get(key=key).user
