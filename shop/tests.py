from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from user_auth.models import User
from shop.models import Products, Retails
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


class TestRetails(APITestCase):
    """
    testing CRUD for Retails
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
        self.product = Products.objects.create(
            name="test_product1",
            model="test_model1",
            date_market_launch="1001-11-11"
        )

    def test_create_retail(self):
        retails_count = Retails.objects.all().count()
        data_retail1 = {
                "name": "Test_retail1",
                "level": "factory",
                "email": "test@mail.ru",
                "country": "Test_country",
                "city": "Test_city",
                "street": "Test_street",
                "house_number": 1,
                "product": self.product.id,
                "obligation": 1800
        }
        url = reverse("retails-list")
        response = self.client.post(url, data_retail1)
        time_created = timezone.localtime().replace(microsecond=0).time()
        retail_name = response.json()['name']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(retails_count + 1, Retails.objects.all().count())
        retail = Retails.objects.get(name=retail_name)
        self.assertEqual(retail.level, data_retail1['level'])
        self.assertEqual(retail.email, data_retail1['email'])
        self.assertEqual(retail.country, data_retail1['country'])
        self.assertEqual(retail.city, data_retail1['city'])
        self.assertEqual(retail.street, data_retail1['street'])
        self.assertEqual(retail.house_number, data_retail1['house_number'])
        self.assertEqual(retail.product.id, data_retail1['product'])
        self.assertEqual(retail.obligation, data_retail1['obligation'])

        # Сравниваем время создания с точностью до секунд
        self.assertEqual(retail.time_created.hour, time_created.hour)
        self.assertEqual(retail.time_created.minute, time_created.minute)
        self.assertEqual(retail.time_created.second, time_created.second)

    def test_get_retail_list(self):
        Retails.objects.create(
                name="Test_retail19",
                level="factory",
                email="test@mail.ru",
                country="Test_country19",
                city="Test_city19",
                street="Test_street",
                house_number=1,
                product=self.product,
                obligation=2400
        )
        Retails.objects.create(
                name="Test_retail20",
                level="factory",
                email="test@mail.ru",
                country="Test_country20",
                city="Test_city20",
                street="Test_street",
                house_number=1,
                product=self.product,
                obligation=1500
        )
        Retails.objects.create(
                name="Test_retail21",
                level="factory",
                email="test@mail.ru",
                country="Test_country21",
                city="Test_city21",
                street="Test_street",
                house_number=1,
                product=self.product,
                obligation=2000
        )
        Retails.objects.create(
                name="Test_retail21",
                level="factory",
                email="test@mail.ru",
                country="Test_country21",
                city="Test_city21",
                street="Test_street",
                house_number=1,
                product=self.product,
                obligation=2000
        )

        retails_count = Retails.objects.all().count()
        url = reverse("retails-list")
        response = self.client.get(url)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', result)
        self.assertIn('results', result)
        self.assertIn('next', result)
        self.assertIn('previous', result)
        self.assertEqual(len(result['results']), retails_count)
        test_country = "Test_country21"

        url_filter = reverse("retails-list") + f"?country={test_country}"
        response = self.client.get(url_filter)
        result = response.json()
        for res in result['results']:
            self.assertEqual(res['country'], test_country)

    def test_update_retail(self):
        self.product2 = Products.objects.create(
            name="test_product2",
            model="test_model2",
            date_market_launch="1001-11-11"
        )
        self.retail11 = Retails.objects.create(
                name="Test_retail11",
                level="factory",
                email="test@mail.ru",
                country="Test_country",
                city="Test_city",
                street="Test_street",
                house_number=1,
                product=self.product,
                obligation=500
        )
        data = {
                "name": "Test_retail2",
                "level": "factory",
                "email": "test_nem@mail.ru",
                "country": "Test_country_new",
                "city": "Test_city_new",
                "street": "Test_street_new",
                "house_number": 12,
                "product": self.product2.id,
                "obligation": 12500
        }
        old_obligation = self.retail11.obligation
        url = reverse("retails-detail", args=[self.retail11.id])
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.retail11.refresh_from_db()
        self.assertEqual(self.retail11.name, data['name'])
        self.assertEqual(self.retail11.email, data['email'])
        self.assertEqual(self.retail11.country, data['country'])
        self.assertEqual(self.retail11.city, data['city'])
        self.assertEqual(self.retail11.street, data['street'])
        self.assertEqual(self.retail11.house_number, data['house_number'])

        # obligation нельзя изменить по API
        self.assertEqual(self.retail11.obligation, old_obligation)

    def test_part_update_retail(self):
        self.product3 = Products.objects.create(
            name="test_product3",
            model="test_model2",
            date_market_launch="1001-11-11"
        )
        self.retail14 = Retails.objects.create(
                name="Test_retail11",
                level="factory",
                email="test@mail.ru",
                country="Test_country",
                city="Test_city",
                street="Test_street",
                house_number=1,
                product=self.product,
                obligation=500
        )
        old_obligation = self.retail14.obligation
        data = {
                "name": "Test_retail18",
                "level": "factory",
                "product": self.product3.id,
        }
        url = reverse("retails-detail", args=[self.retail14.id])
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.retail14.refresh_from_db()
        self.assertEqual(self.retail14.product, self.product3)

        data1 = {
                "name": "Test_retail003",
                "level": "network",
                "obligation": 4500
        }
        url = reverse("retails-detail", args=[self.retail14.id])
        response = self.client.put(url, data1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.retail14.refresh_from_db()

        # obligation нельзя изменить по API
        self.assertEqual(self.retail14.obligation, old_obligation)

    def test_delete_retail(self):
        self.retail15 = Retails.objects.create(
                name="Test_retail15",
                level="factory",
                email="test@mail.ru",
                country="Test_country",
                city="Test_city",
                street="Test_street",
                house_number=1,
                product=self.product,
                obligation=5100
        )
        url = reverse("retails-detail", args=[self.retail15.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retail_validation(self):
        self.retail_val = Retails.objects.create(
                name="Test_retail15",
                level="factory",
                email="test@mail.ru",
                country="Test_country",
                city="Test_city",
                street="Test_street",
                house_number=1,
                product=self.product,
                obligation=5100
        )
        data_retail_val2 = {
                "name": "Test_retail1",
                "level": "factory",
                "email": "test@mail.ru",
                "country": "Test_country",
                "city": "Test_city",
                "street": "Test_street",
                "house_number": 1,
                "product": self.product.id,
                "obligation": 500,
                "supplier": self.retail_val.id
        }
        url = reverse("retails-list")
        response = self.client.post(url, data_retail_val2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['non_field_errors'],
            ['Объект на уровне 0 не может иметь поставщиков!']
            )


class TestRetailsGetLevelAdminAction(APITestCase):
    """
    testing functions get_level, admin_action for Retails
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

    def test_get_level(self):
        """
        testing get_level in model
        """
        self.product = Products.objects.create(
            name="test_product1",
            model="test_model1",
            date_market_launch="1001-11-11"
        )
        self.retail1 = Retails.objects.create(
                name="Test_retail1",
                level="factory",
                email="test@mail.ru",
                country="Test_country",
                city="Test_city",
                street="Test_street",
                house_number=1,
                product=self.product,
                # supplier=None,
                obligation=500
        )
        self.assertEqual(self.retail1.get_level(), 0)

        self.retail2 = Retails.objects.create(
                name="Test_retail2",
                level="factory",
                email="test@mail.ru",
                country="Test_country",
                city="Test_city",
                street="Test_street",
                house_number=1,
                product=self.product,
                supplier=self.retail1,
                obligation=500
        )
        self.assertEqual(self.retail2.get_level(), 1)

        self.retail3 = Retails.objects.create(
                name="Test_retail3",
                level="factory",
                email="test@mail.ru",
                country="Test_country",
                city="Test_city",
                street="Test_street",
                house_number=1,
                product=self.product,
                supplier=self.retail2,
                obligation=500
        )
        self.assertEqual(self.retail3.get_level(), 2)

    def test_admin_action_non_admin(self):
        """
        Доступ только для админа.
        """
        self.product = Products.objects.create(
            name="test_product1",
            model="test_model1",
            date_market_launch="1001-11-11"
        )
        self.retail1 = Retails.objects.create(
                name="Test_retail1",
                level="factory",
                email="test@mail.ru",
                country="Test_country",
                city="Test_city",
                street="Test_street",
                house_number=1,
                product=self.product,
                obligation=500
        )
        url = reverse("admin_action", args=[self.retail1.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.retail1.obligation, 500)


class TestRetailsAdminAction_(APITestCase):
    """
    Проверка для админа метода admin_action
    """
    def test_admin_action(self):
        self.user_admin = create_superuser()
        data = {"email": self.user_admin.email,
                "password": TEST_USER_ADMIN_PASSWORD
                }
        url = reverse('token_obtain_pair')
        self.url_token = url
        response = self.client.post(self.url_token, data)
        self.access_token = response.json().get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.product = Products.objects.create(
            name="test_product1",
            model="test_model1",
            date_market_launch="1001-11-11"
        )
        self.retail1 = Retails.objects.create(
                name="Test_retail1",
                level="factory",
                email="test@mail.ru",
                country="Test_country",
                city="Test_city",
                street="Test_street",
                house_number=1,
                product=self.product,
                obligation=500
        )
        url = reverse("admin_action", args=[self.retail1.id])
        response = self.client.patch(url)
        self.retail1.refresh_from_db()
        self.assertEqual(self.retail1.obligation, 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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

        data = {
            "name": "test_product7",
            "model": "test_model7",
            "date_market_launch": "2023-11-05"
        }
        url = reverse('products-detail', args=[self.product6.pk])
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
    testing CRUD for Products with no active user
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
