from django.db.models.signals import post_save
from django.test import TestCase
from factory.django import mute_signals

from api.models import Image, RegularUser, Thumbnail
from api.tests.test_models.modelsbasesetup import BaseTestSetup


class ImageModelTest(BaseTestSetup, TestCase):
    @mute_signals(post_save)
    def testShouldReturnTrueWhenImageInstanceCreatedInDatabase(self):
        new_user = RegularUser.objects.create_user(**self.test_basic_user)
        new_img = Image.objects.create(
            name="test_image",
            original=self.testing_image,
            uploaded_by=new_user,
        )
        new_thumbnail = Thumbnail.objects.create(
            thumbnail=self.testing_image, image=new_img
        )
        thumbnails = Thumbnail.objects.all()
        self.assertIn(new_thumbnail, thumbnails)
