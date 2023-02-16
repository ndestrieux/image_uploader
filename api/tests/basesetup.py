from api.models import Profile, ThumbnailSize, User
from api.properties import UserTypeChoices


class BaseTestSetup:
    def setUp(self) -> None:
        self.test_basic_user = User.objects.create_user(
            username="basicuser",
            password="password",
            type=UserTypeChoices.BASIC.name,
        )
        self.test_premium_user = User.objects.create_user(
            username="premiumuser",
            password="password",
            type=UserTypeChoices.PREMIUM.name,
        )
        self.test_enterprise_user = User.objects.create_user(
            username="enterpriseuser",
            password="password",
            type=UserTypeChoices.ENTERPRISE.name,
        )
        self.test_custom_user = User.objects.create_user(
            username="customuser",
            password="password",
            type=UserTypeChoices.CUSTOM.name,
        )

    def tearDown(self) -> None:
        pass