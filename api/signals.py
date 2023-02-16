from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Image, Profile, ThumbnailSize, User
from api.properties import (binary_image_properties, original_image_properties,
                            thumbnail_size_properties)
from api.tasks import create_binary_image, create_thumbnail


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.type:
        profile = Profile.objects.create(
            original_image_access=original_image_properties[instance.type],
            binary_image_access=binary_image_properties[instance.type],
            user_id=instance.id,
        )
        for size in thumbnail_size_properties[instance.type]:
            ThumbnailSize.objects.create(size=size, profile=profile)


@receiver(post_save, sender=Image)
def create_alternate_images(sender, instance, created, **kwargs):
    if created:
        user_profile = User.objects.get(id=instance.uploaded_by.id).profile
        thumbnail_sizes = ThumbnailSize.objects.filter(
            profile=user_profile
        ).values_list("size", flat=True)
        if user_profile.binary_image_access:
            create_binary_image(instance.id)
        for size in thumbnail_sizes:
            create_thumbnail(instance.id, size)
