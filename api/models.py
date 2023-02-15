from django.contrib.auth.models import AbstractUser
from django.db import models

from api.properties import UserTypeChoices


class Profile(models.Model):
    original_image_access = models.BooleanField(default=False)
    binary_image_access = models.BooleanField(default=False)


class ThumbnailSize(models.Model):
    size = models.IntegerField()
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="thumbnail_sizes"
    )


class User(AbstractUser):
    type = models.CharField(
        max_length=32, choices=[(tag.name, tag.value) for tag in UserTypeChoices]
    )
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


class Image(models.Model):
    name = models.CharField(max_length=64)
    original = models.ImageField(upload_to="images", max_length=512)
    binary = models.ImageField(
        upload_to="binary_images", max_length=512, blank=True, null=True
    )
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_on = models.DateTimeField(auto_now_add=True)


class Thumbnail(models.Model):
    thumbnail = models.ImageField(upload_to="thumbnails", max_length=512)
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="thumbnails"
    )
