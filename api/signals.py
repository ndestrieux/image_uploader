from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Profile, ThumbnailSize, User
from api.properties import (binary_image_properties, original_image_properties,
                            thumbnail_size_properties)


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
