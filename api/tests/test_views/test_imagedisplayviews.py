from datetime import datetime as dt
from unittest.mock import patch

from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Image, Thumbnail
from api.tests.test_views.viewstestsetup import ViewBaseTestSetup


class ImageDisplayViewsTest(ViewBaseTestSetup, APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_image = ContentFile(b"...", name="test/test.png")
        self.fake_time = dt.fromisoformat("2023-02-13T13:00:00+00:00")
        self.img1 = Image.objects.create(
            name="test", original=self.test_image, uploaded_by=self.test_basic_user
        )
        self.img2 = Image.objects.create(
            name="test",
            original=self.test_image,
            binary=self.test_image,
            binary_expiration_date=self.fake_time,
            uploaded_by=self.test_enterprise_user,
        )
        self.thumb = Thumbnail.objects.create(
            thumbnail=self.test_image, image=self.img2
        )

    def testShouldReturn404WhenDisplayingOriginalImageUploadedByUserWithoutAccess(self):
        response = self.client.get(reverse("image", kwargs={"pk": self.img1.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testShouldReturn200WhenDisplayingOriginalImageUploadedByUserWithAccess(self):
        response = self.client.get(reverse("image", kwargs={"pk": self.img2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        "api.views.timezone.now",
        return_value=dt.fromisoformat("2023-02-13T12:59:00+00:00"),
    )
    def testShouldReturn200WhenDisplayingBinaryImageThatDidNotExpired(self, mock_now):
        response = self.client.get(reverse("binary", kwargs={"pk": self.img2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        "api.views.timezone.now",
        return_value=dt.fromisoformat("2023-02-13T13:01:00+00:00"),
    )
    def testShouldReturn410WhenDisplayingBinaryImageThatHasExpired(self, mock_now):
        response = self.client.get(reverse("binary", kwargs={"pk": self.img2.pk}))
        self.assertEqual(response.status_code, status.HTTP_410_GONE)

    def testShouldReturn200WhenDisplayingThumbnail(self):
        response = self.client.get(reverse("thumbnail", kwargs={"pk": self.thumb.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
