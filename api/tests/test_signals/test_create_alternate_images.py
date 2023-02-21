from unittest.mock import call, patch

from django.test import TestCase

from api.models import Image, RegularUser
from api.tests.test_signals.signalsbasesetup import BaseTestSetup


class CreateAlternateImagesSignalTest(BaseTestSetup, TestCase):
    @patch("api.signals.create_binary_image.delay")
    @patch("api.signals.create_thumbnail.delay")
    def testShouldReturnRightNumberOfTaskCallsWhenBasicUserUploadsImage(
        self, mock_thumbnail_task, mock_binary_image_task
    ):
        user = RegularUser.objects.create_user(**self.test_basic_user)
        img = Image.objects.create(original=self.test_image, uploaded_by=user)
        mock_binary_image_task.assert_has_calls([])
        mock_thumbnail_task.assert_has_calls([call(img.id, 200)])

    @patch("api.signals.create_binary_image.delay")
    @patch("api.signals.create_thumbnail.delay")
    def testShouldReturnRightNumberOfTaskCallsWhenPremiumUserUploadsImage(
        self, mock_thumbnail_task, mock_binary_image_task
    ):
        user = RegularUser.objects.create_user(**self.test_premium_user)
        img = Image.objects.create(original=self.test_image, uploaded_by=user)
        mock_binary_image_task.assert_has_calls([])
        mock_thumbnail_task.assert_has_calls([call(img.id, 200)], [call(img.id, 400)])

    #
    @patch("api.signals.create_binary_image.delay")
    @patch("api.signals.create_thumbnail.delay")
    def testShouldReturnRightNumberOfTaskCallsWhenEnterpriseUserUploadsImage(
        self, mock_thumbnail_task, mock_binary_image_task
    ):
        user = RegularUser.objects.create_user(**self.test_enterprise_user)
        img = Image.objects.create(original=self.test_image, uploaded_by=user)
        mock_binary_image_task.assert_has_calls([call(img.id)])
        mock_thumbnail_task.assert_has_calls([call(img.id, 200)], [call(img.id, 400)])
