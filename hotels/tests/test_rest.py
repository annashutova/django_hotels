from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from hotels_app.models import *
from hotels_app.serializers import *
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
import json


def create_viewset_tests(
    url: str,
    cls_model: models.Model,
    cls_serializer: ModelSerializer,
    request_content: dict,
    to_change: dict,
):
    class ViewSetTests(APITestCase):

        def setUp(self):
            self.user = User.objects.create_user(
                is_superuser=True,
                id=1,
                username='test',
                first_name='test',
                last_name='test',
                email='test@mail.ru',
                password='test'
            )
            token = Token.objects.get(user=self.user)
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            self.model = cls_model.objects.create(**request_content)

        def test_create_instance(self):
            response = self.client.post(url, data=request_content)
            serializer = cls_serializer(data=request_content)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_retrive_instance(self):
            url_to_get = f'{url}{self.model.id}/'
            response = self.client.get(url_to_get)
            serializer = cls_serializer(data=request_content)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_update_instance(self):
            url_to_update = f'{url}{self.model.id}/'
            response = self.client.put(
                url_to_update,
                data=json.dumps(to_change),
                content_type='application/json'
            )
            serializer = cls_serializer(data=to_change)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_delete_instance(self):
            url_to_delete = f'{url}{self.model.id}/'
            response = self.client.delete(url_to_delete)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertFalse(
                cls_model.objects.filter(id=self.model.id).exists()
            )

    return ViewSetTests


HotelViewTests = create_viewset_tests(
    '/rest/hotel/',
    Hotel,
    HotelSerializer,
    {
    "company": "company",
    "name": "name",
    "star_rating": 4,
    "country": "country",
    "state": "state",
    "city": "city",
    "street": "street",
    "building": "1",
    "latitude": 59.842725,
    "longitude": 30.31841
    },
    {
    "company": "new_company",
    "name": "new_name",
    "star_rating": 5,
    "country": "new_country",
    "state": "new_state",
    "city": "new_city",
    "street": "new_street",
    "building": "2",
    "latitude": 59,
    "longitude": 30
    },
    )
