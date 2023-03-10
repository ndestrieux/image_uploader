"""config URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from api.views import (BinaryImageView, ImageListAPIView, OriginalImageView,
                       ThumbnailView, UploadImageView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("authtoken/", ObtainAuthToken.as_view(), name="auth-token"),
    path("upload/", UploadImageView.as_view(), name="upload"),
    path("image_list/", ImageListAPIView.as_view(), name="image-list"),
    path("image_list/image/<int:pk>/", OriginalImageView.as_view(), name="image"),
    path("image_list/binary/<int:pk>/", BinaryImageView.as_view(), name="binary"),
    path("image_list/thumbnail/<int:pk>/", ThumbnailView.as_view(), name="thumbnail"),
]
