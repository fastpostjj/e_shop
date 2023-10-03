from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from user_auth.models import User
from shop.models import Products, Retails
from rest_framework import status
from datetime import time


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
    """
    testing CRUD for Products
    """
    def setUp(self):
        self.user = create_user()
        data = {"email": self.user.email,
                "password": TEST_USER_PASSWORD
                }
        url = reverse('token_obtain_pair')
        self.url_token = url
        response = self.client.post(self.url_token, data)
        self.access_token = response.json().get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_get_product_list(self):
        products_count = Products.objects.all().count()
        self.product1 = Products.objects.create(
            name="test_product1",
            model="test_model1",
            date_market_launch="1001-11-11"
        )
        Products.objects.create(
            name="test_product1",
            model="test_model1",
            date_market_launch="2001-01-01"
        )
        Products.objects.create(
            name="test_product2",
            model="test_model2",
            date_market_launch="2002-02-02"
        )
        Products.objects.create(
            name="test_product3",
            model="test_model3",
            date_market_launch="2003-03-03"
        )
        Products.objects.create(
            name="test_product4",
            model="test_model4",
            date_market_launch="2004-04-04"
        )
        Products.objects.create(
            name="test_product5",
            model="test_model5",
            date_market_launch="2005-05-05"
        )
        url = reverse('products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertEqual(result['count'], products_count + 6)
        self.assertIn('count', result)
        self.assertTrue('next', result)
        self.assertTrue('previous', result)
        self.assertEqual(result['results'][0]['name'], self.product1.name)
        self.assertEqual(result['results'][0]['model'], self.product1.model)
        self.assertEqual(result['results'][0]['date_market_launch'], self.product1.date_market_launch)

    def test_create_product(self):
        products_count = Products.objects.all().count()
        url = reverse('products-list')
        data = {
            "name": "test_product",
            "model": "test_model",
            "date_market_launch": "2023-11-05"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Products.objects.all().count(), products_count + 1)

    def test_update_product(self):
        self.product6 = Products.objects.create(
            name="test_product6",
            model="test_model6",
            date_market_launch="1001-11-11"
        )
        url = reverse('products-detail', args=[self.product6.pk])

        data = {
            "name": "test_product7",
            "model": "test_model7",
            "date_market_launch": "2023-11-05"
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['name'], data['name'])
        self.assertEqual(result['model'], data['model'])
        self.assertEqual(result['date_market_launch'], data['date_market_launch'])

    def test_part_update_product(self):
        self.product8 = Products.objects.create(
            name="test_product8",
            model="test_model8",
            date_market_launch="1001-12-12"
        )
        url = reverse('products-detail', args=[self.product8.pk])

        data1 = {
            "name": "test_product9"
        }
        data2 = {
            "name": "test_product10",
            "model": "test_model9"
        }
        data3 = {
            "name": "test_product11",
            "date_market_launch": "2028-11-05"
        }
        response = self.client.put(url, data1)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['name'], data1['name'])

        response = self.client.put(url, data2)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['model'], data2['model'])

        response = self.client.put(url, data3)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['date_market_launch'], data3['date_market_launch'])

    def test_delete_product(self):
        self.product10 = Products.objects.create(
            name="test_product10",
            model="test_model10",
            date_market_launch="1001-12-12"
        )
        url = reverse('products-detail', args=[self.product10.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestProductsNoActiveUser(APITestCase):
    """
    testing CRUD for Products
    """
    def setUp(self):
        self.user = create_user_not_active()
        data = {"email": self.user.email,
                "password": TEST_USER_PASSWORD_NO_ACTIVE
                }
        url = reverse('token_obtain_pair')
        self.url_token = url
        response = self.client.post(self.url_token, data)
        self.access_token = response.json().get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_get_product_list_no_active_user(self):
        self.product1 = Products.objects.create(
            name="test_product1",
            model="test_model1",
            date_market_launch="1001-11-11"
        )
        url = reverse('products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_no_active_user(self):
        url = reverse('products-list')
        data = {
            "name": "test_product",
            "model": "test_model",
            "date_market_launch": "2023-11-05"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_product(self):
        self.product6 = Products.objects.create(
            name="test_product6",
            model="test_model6",
            date_market_launch="1001-11-11"
        )
        url = reverse('products-detail', args=[self.product6.pk])

        data = {
            "name": "test_product7",
            "model": "test_model7",
            "date_market_launch": "2023-11-05"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_product(self):
        self.product10 = Products.objects.create(
            name="test_product10",
            model="test_model10",
            date_market_launch="1001-12-12"
        )
        url = reverse('products-detail', args=[self.product10.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
