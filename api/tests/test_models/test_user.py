from django.db.models.signals import post_save
from django.test import TestCase
from factory.django import mute_signals

from api.models import User
from api.tests.basesetup import BaseTestSetup


class UserModelTest(BaseTestSetup, TestCase):
    @mute_signals(post_save)
    def testShouldReturnTrueWhenUserInstanceCreatedInDatabase(self):
        new_user = User.objects.create_user(**self.test_basic_user)
        users = User.objects.all()
        self.assertIn(new_user, users)
