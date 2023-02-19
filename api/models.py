import random
import re
import string
from datetime import datetime as dt

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from api.properties import UserTypeChoices


class User(AbstractUser):
    type = models.CharField(
        max_length=32,
        choices=[(tag.name, tag.value) for tag in UserTypeChoices],
        default=UserTypeChoices.CUSTOM.name,
    )


class RegularUserManager(UserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                type__in=[choice.name for choice in UserTypeChoices][:-1],
                is_superuser=False,
            )
        )


class RegularUser(User):
    objects = RegularUserManager()

    class Meta:
        proxy = True


class CustomUserManager(UserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(type=UserTypeChoices.CUSTOM.name, is_superuser=False)
        )


class CustomUser(User):
    objects = CustomUserManager()

    class Meta:
        proxy = True


class Profile(models.Model):
    original_image_access = models.BooleanField(default=False)
    binary_image_access = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ThumbnailSize(models.Model):
    size = models.PositiveIntegerField()
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="thumbnail_sizes"
    )


class Image(models.Model):
    name = models.CharField(max_length=64)
    original = models.ImageField(upload_to="images", max_length=512)
    binary = models.ImageField(
        upload_to="binary_images", max_length=512, blank=True, null=True
    )
    binary_expiration_date = models.DateTimeField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.pk is None:
            self.original.name = self.rename_image_file(self.original.name)
        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    def rename_image_file(self, filename):
        ext = filename.split(".")[-1]
        if ext.lower() == "jpg":
            ext = "jpeg"
        time_stamp = dt.now().strftime("%Y%m%d%H%M%S")
        random_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=9))
        name = re.sub(r"[^\w]+", "-", self.name.lower())
        filename = f"{time_stamp}-{random_id}-{name}.{ext}"
        return filename


class Thumbnail(models.Model):
    thumbnail = models.ImageField(upload_to="thumbnails", max_length=512)
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="thumbnails"
    )
