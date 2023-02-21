import re
from io import BytesIO

from celery import shared_task
from django.core.files import File
from PIL import Image as PilImg

from api.models import Image, Thumbnail


@shared_task
def create_thumbnail(image_id: int, size: int) -> str:
    img_instance = Image.objects.get(id=image_id)
    img = img_instance.original
    thumb = PilImg.open(img)
    left, top, right, bottom = 0, 0, size, size
    if thumb.width > thumb.height:
        output_size = (thumb.width, size)
        thumb.thumbnail(output_size, PilImg.ANTIALIAS)
        left = (thumb.width - size) // 2
        right = thumb.width - left
        thumb = thumb.crop((left, top, right, bottom))
    elif thumb.width < thumb.height:
        output_size = (size, thumb.height)
        thumb.thumbnail(output_size, PilImg.ANTIALIAS)
        top = (thumb.height - size) // 2
        bottom = thumb.height - top
        thumb = thumb.crop((left, top, right, bottom))
    else:
        output_size = (size, size)
        thumb.thumbnail(output_size, PilImg.ANTIALIAS)
    buffer = BytesIO()
    name, extension = re.split(r"[/.]", img.name)[-2:]
    thumb.save(buffer, format=extension)
    thumb = File(buffer, name=f"{img_instance.uploaded_by}/{name}-tb{size}.{extension}")
    Thumbnail.objects.create(thumbnail=thumb, image=img_instance)
    return "Thumbnail created successfully!"


@shared_task
def create_binary_image(image_id: int) -> str:
    img_instance = Image.objects.get(id=image_id)
    img = img_instance.original
    binary_img = PilImg.open(img)
    binary_img = binary_img.convert("1")
    buffer = BytesIO()
    name, extension = re.split(r"[/.]", img.name)[-2:]
    binary_img.save(buffer, format=extension)
    binary_img = File(
        buffer, name=f"{img_instance.uploaded_by}/{name}-binary.{extension}"
    )
    img_instance.binary = binary_img
    img_instance.save(update_fields=["binary"])
    return "Binary image created successfully!"
