from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Image, Profile, RegularUser, ThumbnailSize, User
from api.properties import profile_properties
from api.tasks import create_binary_image, create_thumbnail


@receiver(post_save, sender=RegularUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            original_image_access=profile_properties[instance.type][
                "original_image_access"
            ],
            binary_image_access=profile_properties[instance.type][
                "binary_image_access"
            ],
            user_id=instance.id,
        )
        for size in profile_properties[instance.type]["thumbnail_sizes"]:
            ThumbnailSize.objects.create(size=size, profile=profile)


@receiver(post_save, sender=Image)
def create_alternate_images(sender, instance, created, **kwargs):
    if created:
        user_profile = User.objects.get(id=instance.uploaded_by.id).profile
        thumbnail_sizes = ThumbnailSize.objects.filter(
            profile=user_profile
        ).values_list("size", flat=True)
        if user_profile.binary_image_access:
            create_binary_image.delay(instance.id)
        for size in thumbnail_sizes:
            create_thumbnail.delay(instance.id, size)
