from django.core.files.base import ContentFile

from api.models import Image, Thumbnail
from api.properties import UserTypeChoices


class BaseTestSetup:
    def setUp(self) -> None:
        self.test_basic_user = {
            "username": "basicuser",
            "password": "password",
            "type": UserTypeChoices.BASIC.name,
        }
        self.test_premium_user = {
            "username": "premiumuser",
            "password": "password",
            "type": UserTypeChoices.PREMIUM.name,
        }
        self.test_enterprise_user = {
            "username": "enterpriseuser",
            "password": "password",
            "type": UserTypeChoices.ENTERPRISE.name,
        }
        self.test_custom_user = {
            "username": "customuser",
            "password": "password",
            "type": UserTypeChoices.CUSTOM.name,
        }
        self.testing_image = ContentFile(b"...", name="test.png")

    @classmethod
    def tearDownClass(cls) -> None:
        images = Image.objects.all()
        thumbnails = Thumbnail.objects.all()
        for img in images:
            img.original.delete()
            img.binary.delete()
        for thumb in thumbnails:
            thumb.thumbnail.delete()
