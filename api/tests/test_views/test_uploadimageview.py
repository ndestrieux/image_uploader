import io

from django.urls import reverse
from PIL import Image as PilImg
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.tests.test_views.viewstestsetup import ViewBaseTestSetup


class UploadImageViewTest(ViewBaseTestSetup, APITestCase):
    def generate_image_test_file(self):
        file = io.BytesIO()
        image = PilImg.new("RGBA", size=(800, 700), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "image_test.png"
        file.seek(0)
        return file

    def generate_non_image_test_file(self):
        file = io.StringIO("not_an_image.txt")
        return file

    def testShouldReturn201WhenCorrectImageFormatUploaded(self):
        token = Token.objects.get(user=self.test_basic_user)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {"name": "test_file", "image": self.generate_image_test_file()}
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testShouldReturn400WhenIncorrectImageFormatUploaded(self):
        token = Token.objects.get(user=self.test_basic_user)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            "name": "test_file",
            "image": self.generate_non_image_test_file(),
        }
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testShouldReturn401WhenUnauthorizedUserUploadFile(self):
        header = {"HTTP_AUTHORIZATION": f"Token unknown"}
        data = {
            "name": "test_file",
            "image": self.generate_image_test_file(),
        }
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testShouldReturn201WhenPremiumUserUploadFile(self):
        token = Token.objects.get(user=self.test_premium_user)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            "name": "test_file",
            "image": self.generate_image_test_file(),
        }
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testShouldReturn201WhenEnterpriseUserUploadFileWithBinaryExpireTimeFieldInRange(
        self,
    ):
        token = Token.objects.get(user=self.test_enterprise_user)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            "name": "test_file",
            "image": self.generate_image_test_file(),
            "binary_expire_time": 3000,
        }
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testShouldReturn400WhenEnterpriseUserUploadFileWithBinaryExpireTimeFieldOutOfRange(
        self,
    ):
        token = Token.objects.get(user=self.test_enterprise_user)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            "name": "test_file",
            "image": self.generate_image_test_file(),
            "binary_expire_time": 200,
        }
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testShouldReturn400WhenEnterpriseUserUploadFileWithoutBinaryExpireTimeField(
        self,
    ):
        token = Token.objects.get(user=self.test_enterprise_user)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            "name": "test_file",
            "image": self.generate_image_test_file(),
        }
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testShouldReturn201WhenCustomUserWithBinaryFileAccessUploadFileWithBinaryExpireTimeField(
        self,
    ):
        token = Token.objects.get(user=self.test_custom_user_with_binary_image)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            "name": "test_file",
            "image": self.generate_image_test_file(),
            "binary_expire_time": 3000,
        }
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testShouldReturn400WhenCustomUserWithBinaryFileAccessUploadFileWithoutBinaryExpireTimeField(
        self,
    ):
        token = Token.objects.get(user=self.test_custom_user_with_binary_image)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            "name": "test_file",
            "image": self.generate_image_test_file(),
        }
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testShouldReturn201WhenCustomUserWithoutBinaryFileAccessUploadFileWithoutBinaryExpireTimeField(
        self,
    ):
        token = Token.objects.get(user=self.test_custom_user_without_binary_image)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            "name": "test_file",
            "image": self.generate_image_test_file(),
        }
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testShouldReturn400WhenCustomUserWithoutBinaryFileAccessUploadFileWithBinaryExpireTimeField(
        self,
    ):
        token = Token.objects.get(user=self.test_custom_user_without_binary_image)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            "name": "test_file",
            "image": self.generate_image_test_file(),
            "binary_expire_time": 3000,
        }
        response = self.client.post(
            reverse("upload"), format="multipart", data=data, **header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
