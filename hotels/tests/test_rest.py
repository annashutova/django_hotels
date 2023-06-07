from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from hotels_app.models import Room, Hotel, models
from hotels_app.serializers import HotelSerializer, ModelSerializer
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
                password='test',
            )
            token = Token.objects.get(user=self.user)
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
            self.model = cls_model.objects.create(**request_content)

        def test_create_instance(self):
            response = self.client.post(url, data=request_content)
            serializer = cls_serializer(data=request_content)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_retrive_instance(self):
            url_to_get = '{url}{model_id}/'.format(url=url, model_id=self.model.id)
            response = self.client.get(url_to_get)
            serializer = cls_serializer(data=request_content)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_update_instance(self):
            url_to_update = '{url}{model_id}/'.format(url=url, model_id=self.model.id)
            response = self.client.put(
                url_to_update,
                data=json.dumps(to_change),
                content_type='application/json',
            )
            serializer = cls_serializer(data=to_change)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_delete_instance(self):
            url_to_delete = '{url}{model_id}/'.format(url=url, model_id=self.model.id)
            response = self.client.delete(url_to_delete)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertFalse(
                cls_model.objects.filter(id=self.model.id).exists(),
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
        "longitude": 30.31841,
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
        "longitude": 30,
    },
)


class RoomTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            email='test@mail.ru',
            password='test',
        )
        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.request_data = {
            "hotel": {
                "company": "company",
                "name": "name",
                "star_rating": 4,
                "country": "country",
                "state": "state",
                "city": "city",
                "street": "street",
                "building": "1",
                "latitude": 59.842725,
                "longitude": 30.31841,
            },
            "type": "Standart",
            "code": "909",
            "price": 1000,
            "capacity": 2,
            "double_bed": 1,
            "single_bed": 1,
            "safe": True,
            "tv": True,
            "soundproofing": True,
            "telephone": True,
            "heating": True,
            "wardrobe": True,
            "shower": True,
            "minibar": True,
            "air_conditioning": True,
            "bath": True,
            "desk": True,
        }
        self.model = Room.objects.create(
            hotel=Hotel.objects.create(
                company="company",
                name="name",
                star_rating=4,
                country="country",
                state="state",
                city="city",
                street="street",
                building="1",
                latitude=59.842725,
                longitude=30.31841,
            ),
            type="Standart",
            code="909",
            price=1000,
            capacity=2,
            double_bed=1,
            single_bed=1,
            safe=True,
            tv=True,
            soundproofing=True,
            telephone=True,
            heating=True,
            wardrobe=True,
            shower=True,
            minibar=True,
            air_conditioning=True,
            bath=True,
            desk=True,
        )
        self.to_change = {
            "type": "Suite",
            "code": "909",
            "price": 1000,
            "capacity": 2,
            "double_bed": 1,
            "single_bed": 1,
            "safe": True,
            "tv": True,
            "soundproofing": False,
            "telephone": True,
            "heating": True,
            "wardrobe": True,
            "shower": True,
            "minibar": True,
            "air_conditioning": True,
            "bath": True,
            "desk": True,
        }

    def test_get_model(self):
        url_to_get = '/rest/room/{model_id}/'.format(model_id=self.model.id)
        response = self.client.get(url_to_get)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        url_to_update = '/rest/room/{model_id}/'.format(model_id=self.model.id)
        response = self.client.patch(
            url_to_update,
            data=json.dumps(
                self.to_change,
            ),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_model(self):
        url_to_delete = '/rest/room/{model_id}/'.format(model_id=self.model.id)
        response = self.client.delete(url_to_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Room.objects.filter(id=self.model.id).exists(),
        )
