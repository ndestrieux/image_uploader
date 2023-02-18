from django.test import TestCase

from api.models import Profile, RegularUser, ThumbnailSize
from api.tests.basesetup import BaseTestSetup


class UserSignalTest(BaseTestSetup, TestCase):
    def testShouldReturnTrueWhenProfileCreatedAlongWithUser(self):
        new_user = RegularUser.objects.create_user(**self.test_basic_user)
        user_id_list = Profile.objects.all().values_list("user", flat=True)
        self.assertIn(new_user.id, user_id_list)

    def testShouldReturnTrueWhenProfileCreatedProperlyForBasicUser(self):
        new_basic_user = RegularUser.objects.create_user(**self.test_basic_user)
        basic_user_profile = Profile.objects.get(user=new_basic_user.id)
        thumbnail_sizes = list(
            ThumbnailSize.objects.filter(profile=basic_user_profile.id).values_list(
                "size", flat=True
            )
        )
        self.assertEqual(basic_user_profile.original_image_access, False)
        self.assertEqual(basic_user_profile.binary_image_access, False)
        self.assertEqual(thumbnail_sizes, [200])

    def testShouldReturnTrueWhenProfileCreatedProperlyForPremiumUser(self):
        new_premium_user = RegularUser.objects.create_user(**self.test_premium_user)
        premium_user_profile = Profile.objects.get(user=new_premium_user.id)
        thumbnail_sizes = list(
            ThumbnailSize.objects.filter(profile=premium_user_profile.id).values_list(
                "size", flat=True
            )
        )
        self.assertEqual(premium_user_profile.original_image_access, True)
        self.assertEqual(premium_user_profile.binary_image_access, False)
        self.assertEqual(thumbnail_sizes, [200, 400])

    def testShouldReturnTrueWhenProfileCreatedProperlyForEnterpriseUser(self):
        new_enterprise_user = RegularUser.objects.create_user(
            **self.test_enterprise_user
        )
        enterprise_user_profile = Profile.objects.get(user=new_enterprise_user.id)
        thumbnail_sizes = list(
            ThumbnailSize.objects.filter(
                profile=enterprise_user_profile.id
            ).values_list("size", flat=True)
        )
        self.assertEqual(enterprise_user_profile.original_image_access, True)
        self.assertEqual(enterprise_user_profile.binary_image_access, True)
        self.assertEqual(thumbnail_sizes, [200, 400])
