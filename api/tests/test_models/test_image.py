from django.db.models.signals import post_save
from django.test import TestCase
from factory.django import mute_signals

from api.models import Image, User
from api.tests.basesetup import BaseTestSetup


class ImageModelTest(BaseTestSetup, TestCase):
    @mute_signals(post_save)
    def testShouldReturnTrueWhenImageInstanceCreatedInDatabase(self):
        new_user = User.objects.create_user(**self.test_basic_user)
        new_img = Image.objects.create(
            original=self.testing_image,
            uploaded_by=new_user,
        )
        images = Image.objects.all()
        self.assertIn(new_img, images)
