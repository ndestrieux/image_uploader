from unittest.mock import patch

from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import Image, User
from api.tests.test_views.viewstestsetup import ViewBaseTestSetup


class ImageListAPIViewTest(ViewBaseTestSetup, APITestCase):
    @patch("celery.app.task.Task.delay")
    def setUp(self, mock_task) -> None:
        super().setUp()
        self.test_image = ContentFile(b"...", name="test/test.png")
        self.users = User.objects.all()
        for user in self.users:
            Token.objects.create(user=user)
            Image.objects.create(
                name="test", original=self.test_image, uploaded_by=user
            )

    def testShouldReturn200AndCorrectDataWhenBasicUserRequests(self):
        token = Token.objects.get(user=self.test_basic_user)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        response = self.client.get(reverse("image-list"), format="multipart", **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("thumbnails", response.data[0].keys())
        self.assertNotIn("image", response.data[0].keys())
        self.assertNotIn("binary", response.data[0].keys())

    def testShouldReturn200AndCorrectDataWhenPremiumUserRequests(self):
        token = Token.objects.get(user=self.test_premium_user)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        response = self.client.get(reverse("image-list"), format="multipart", **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("thumbnails", response.data[0].keys())
        self.assertIn("image", response.data[0].keys())
        self.assertNotIn("binary", response.data[0].keys())

    def testShouldReturn200AndCorrectDataWhenEnterpriseUserRequests(self):
        token = Token.objects.get(user=self.test_enterprise_user)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        response = self.client.get(reverse("image-list"), format="multipart", **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("thumbnails", response.data[0].keys())
        self.assertIn("image", response.data[0].keys())
        self.assertIn("binary", response.data[0].keys())
