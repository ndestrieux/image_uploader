import shutil
from glob import glob

from django.conf import settings
from rest_framework.authtoken.models import Token

from api.models import CustomUser, Profile, RegularUser, User
from api.properties import UserTypeChoices


class ViewBaseTestSetup:
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_basic_user = RegularUser.objects.create_user(
            username="test_basic_user",
            password="password",
            type=UserTypeChoices.BASIC.name,
        )
        cls.test_premium_user = RegularUser.objects.create_user(
            username="test_premium_user",
            password="password",
            type=UserTypeChoices.PREMIUM.name,
        )
        cls.test_enterprise_user = RegularUser.objects.create_user(
            username="test_enterprise_user",
            password="password",
            type=UserTypeChoices.ENTERPRISE.name,
        )
        cls.test_custom_user_with_binary_image = CustomUser.objects.create_user(
            username="test_custom_user_with_binary_image",
            password="password",
            type=UserTypeChoices.CUSTOM.name,
        )
        cls.test_custom_profile_with_binary_image = Profile.objects.create(
            binary_image_access=True, user=cls.test_custom_user_with_binary_image
        )
        cls.test_custom_user_without_binary_image = CustomUser.objects.create_user(
            username="test_custom_user_without_binary_image",
            password="password",
            type=UserTypeChoices.CUSTOM.name,
        )
        cls.test_custom_profile_without_binary_image = Profile.objects.create(
            user=cls.test_custom_user_without_binary_image
        )
        cls.users = User.objects.all()
        for user in cls.users:
            Token.objects.create(user=user)

    @classmethod
    def tearDownClass(cls) -> None:
        for match in glob(settings.MEDIA_ROOT + "/*/test*"):
            shutil.rmtree(match, ignore_errors=True)
