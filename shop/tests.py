from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from user_auth.models import User
from shop.models import Products, Retails
from django.utils import timezone

from rest_framework import status


TEST_USER_EMAIL = "test@email.tu"
TEST_USER_PASSWORD = "password_user"
TEST_USER_EMAIL_NO_ACTIVE = "testno@email.tu"
TEST_USER_PASSWORD_NO_ACTIVE = "password_user_no_active"
TEST_USER_ADMIN_EMAIL = "test_admin@email.tu"
TEST_USER_ADMIN_PASSWORD = "password_admin"


# создание пользователей для тестирования
def create_superuser(*args, **options):
    user = User.objects.create(
        email=TEST_USER_ADMIN_EMAIL,
        first_name='Admin',
        last_name='SuperAdmin',
        is_staff=True,
        is_superuser=True
    )
    user.set_password(TEST_USER_ADMIN_PASSWORD)
    user.save()
    return user


def create_user(*args, **options):
    user = User.objects.create(
        email=TEST_USER_EMAIL,
        first_name='User',
        last_name='Just User',
        is_staff=False,
        is_superuser=False
    )
    user.set_password(TEST_USER_PASSWORD)
    user.save()
    return user


def create_user_not_active(*args, **options):
    user = User.objects.create(
        email=TEST_USER_EMAIL_NO_ACTIVE,
        first_name='User',
        last_name='Just User',
        is_staff=False,
        is_superuser=False,
        is_active=False
    )
    user.set_password(TEST_USER_PASSWORD_NO_ACTIVE)
    user.save()
    return user


class TestProducts(APITestCase):
    def setUp(self):
        self.user = create_user()
        data = {"email": self.user.email,
                "password": TEST_USER_PASSWORD
        }
        self.url_token = reverse('token_obtain_pair')
        response = self.client.post(self.url_token, data)
        self.access_token = response.json().get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_product(self):
        products_count = Products.objects.all().count()
        url = reverse('shop_products_create')
        data = {
            "name": "test_product",
            "model": "test_model",
            "date_market_launch": timezone.now()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Products.objects.all().count(), products_count + 1)
