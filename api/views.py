from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Image
from api.serializers import ImageListSerializer, UploadImageSerializer


class UploadImageView(CreateAPIView):
    serializer_class = UploadImageSerializer
    permission_classes = (IsAuthenticated,)

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
        key = self.request.META.get("HTTP_AUTHORIZATION").split()[-1]
        context["uploaded_by"] = Token.objects.get(key=key).user
        return context


class ImageListAPIView(ListAPIView):
    serializer_class = ImageListSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.get_authorized_user()
        return context

    def get_queryset(self):
        return Image.objects.filter(uploaded_by=self.get_authorized_user())

    def get_authorized_user(self):
        key = self.request.META.get("HTTP_AUTHORIZATION").split()[-1]
        return Token.objects.get(key=key).user
