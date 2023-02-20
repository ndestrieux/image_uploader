import shutil
from glob import glob

from django.conf import settings
from django.core.files.base import ContentFile

from api.properties import UserTypeChoices


class BaseTestSetup:
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_basic_user = {
            "username": "test_basic_user",
            "password": "password",
            "type": UserTypeChoices.BASIC.name,
        }
        cls.test_premium_user = {
            "username": "test_premium_user",
            "password": "password",
            "type": UserTypeChoices.PREMIUM.name,
        }
        cls.test_enterprise_user = {
            "username": "test_enterprise_user",
            "password": "password",
            "type": UserTypeChoices.ENTERPRISE.name,
        }
        cls.test_image = ContentFile(b"...", name="test/test.png")

    @classmethod
    def tearDownClass(cls) -> None:
        for match in glob(settings.MEDIA_ROOT + "/*/test*"):
            shutil.rmtree(match, ignore_errors=True)
