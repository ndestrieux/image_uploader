from django.test import TestCase

from api.models import Profile, ThumbnailSize, User
from api.tests.basesetup import BaseTestSetup


class UserModelTest(BaseTestSetup, TestCase):
    def testShouldReturnTrueWhenUserInstanceCreatedInDatabase(self):
        users = User.objects.all()
        self.assertIn(self.test_basic_user, users)

    def testShouldReturnTrueWhenProfileCreatedAlongWithUser(self):
        user_id_list = Profile.objects.all().values_list("user", flat=True)
        self.assertIn(self.test_basic_user.id, user_id_list)

    def testShouldReturnTrueWhenProfileCreatedProperlyForBasicUser(self):
        basic_user_profile = Profile.objects.get(user=self.test_basic_user.id)
        thumbnail_sizes = list(
            ThumbnailSize.objects.filter(profile=basic_user_profile.id).values_list(
                "size", flat=True
            )
        )
        self.assertEqual(basic_user_profile.original_image_access, False)
        self.assertEqual(basic_user_profile.binary_image_access, False)
        self.assertEqual(thumbnail_sizes, [200])

    def testShouldReturnTrueWhenProfileCreatedProperlyForPremiumUser(self):
        premium_user_profile = Profile.objects.get(user=self.test_premium_user.id)
        thumbnail_sizes = list(
            ThumbnailSize.objects.filter(profile=premium_user_profile.id).values_list(
                "size", flat=True
            )
        )
        self.assertEqual(premium_user_profile.original_image_access, True)
        self.assertEqual(premium_user_profile.binary_image_access, False)
        self.assertEqual(thumbnail_sizes, [200, 400])

    def testShouldReturnTrueWhenProfileCreatedProperlyForEnterpriseUser(self):
        enterprise_user_profile = Profile.objects.get(user=self.test_enterprise_user.id)
        thumbnail_sizes = list(
            ThumbnailSize.objects.filter(
                profile=enterprise_user_profile.id
            ).values_list("size", flat=True)
        )
        self.assertEqual(enterprise_user_profile.original_image_access, True)
        self.assertEqual(enterprise_user_profile.binary_image_access, True)
        self.assertEqual(thumbnail_sizes, [200, 400])

    def testShouldReturnTrueWhenProfileCreatedProperlyForCustomUser(self):
        custom_user_profile = Profile.objects.get(user=self.test_custom_user.id)
        thumbnail_sizes = list(
            ThumbnailSize.objects.filter(profile=custom_user_profile.id).values_list(
                "size", flat=True
            )
        )
        self.assertEqual(custom_user_profile.original_image_access, False)
        self.assertEqual(custom_user_profile.binary_image_access, False)
        self.assertEqual(thumbnail_sizes, [])
