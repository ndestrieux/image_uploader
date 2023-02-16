from django.db.models.signals import post_save
from django.test import TestCase
from factory.django import mute_signals

from api.models import Profile, ThumbnailSize, User
from api.tests.basesetup import BaseTestSetup


class UserModelTest(BaseTestSetup, TestCase):
    @mute_signals(post_save)
    def testShouldReturnTrueWhenUserInstanceCreatedInDatabase(self):
        new_user = User.objects.create_user(**self.test_basic_user)
        new_profile = Profile.objects.create(user=new_user)
        thumbnail_sizes = ThumbnailSize.objects.all()
        new_tn_size = ThumbnailSize.objects.create(size=200, profile=new_profile)
        self.assertIn(new_tn_size, thumbnail_sizes)
