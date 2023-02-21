import shutil
from glob import glob

from django.conf import settings
from django.core.files.base import ContentFile

from api.properties import UserTypeChoices


class BaseTestSetup:
    def setUp(self) -> None:
        self.test_basic_user = {
            "username": "test_basic_user",
            "password": "password",
            "type": UserTypeChoices.BASIC.name,
        }
        self.testing_image = ContentFile(b"...", name="test/test.png")

    @classmethod
    def tearDownClass(cls) -> None:
        for match in glob(settings.MEDIA_ROOT + "/*/test*"):
            shutil.rmtree(match, ignore_errors=True)
