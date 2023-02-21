import shutil
from glob import glob

from django.conf import settings

from api.models import RegularUser
from api.properties import UserTypeChoices


class ViewBaseTestSetup:
    def setUp(self) -> None:
        self.test_basic_user = RegularUser.objects.create_user(
            username="test_basic_user",
            password="password",
            type=UserTypeChoices.BASIC.name,
        )
        self.test_premium_user = RegularUser.objects.create_user(
            username="test_premium_user",
            password="password",
            type=UserTypeChoices.PREMIUM.name,
        )
        self.test_enterprise_user = RegularUser.objects.create_user(
            username="test_enterprise_user",
            password="password",
            type=UserTypeChoices.ENTERPRISE.name,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        for match in glob(settings.MEDIA_ROOT + "/*/test*"):
            shutil.rmtree(match, ignore_errors=True)
