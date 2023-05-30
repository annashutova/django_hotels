from django.test import TestCase
from  django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test.client import Client
from hotels_app.models import Amenity, Hotel, Room
from rest_framework import status
from rest_framework.test import APIClient
from json import dumps


def create_viewset_tests(url, cls_model, request_data, attr, attr_value, hotel=None):
    class ViewSetTests(TestCase):

        def setUp(self) -> None:
            self.client = Client()
            self.creds_user = {'username': 'user', 'password': 'user'}
            self.creds_superuser = {'username': 'superuser', 'password': 'superuser'}
            self.user = User.objects.create_user(**self.creds_user)
            self.superuser = User.objects.create_user(is_superuser=True, **self.creds_superuser)
            self.superuser_token = Token.objects.get(user=self.superuser)
            self.request_data = request_data
            if cls_model == Room:
                self.hotel_instance = Hotel.objects.create(**hotel)
                hotel['id'] = self.hotel_instance.id
                self.request_data['hotel'] = self.hotel_instance

        def test_rest_superuser(self):
            # superuser logging in
            self.client.login(**self.creds_superuser)

            # GET
            resp_get = self.client.get(url)
            self.assertEqual(resp_get.status_code, status.HTTP_200_OK)

            #POST
            resp_post = self.client.post(url, data=self.request_data)
            self.assertEqual(resp_post.status_code, status.HTTP_201_CREATED)

            #PUT
            created = cls_model.objects.get(**self.request_data)
            url_to_created = f'{url}{created.id}/'
            self.request_data[attr] = attr_value
            resp_put = self.client.put(url_to_created, format='multipart', data=self.request_data)
            self.assertEqual(resp_put.status_code, status.HTTP_200_OK)
            after_put = cls_model.object.get(id=created.id)
            self.assertEqual(getattr(after_put, attr), attr_value)

            # DELETE EXISTING
            resp_delete = self.client.delete(url_to_created)
            self.assertEqual(resp_delete.status_code, status.HTTP_204_NO_CONTENT)

            # DELETE NONEXISTING
            resp_delete = self.client.delete(url_to_created)
            self.assertEqual(resp_delete.status_code, status.HTTP_404_NOT_FOUND)

            # superuser logging out
            self.client.logout()
            if cls_model == Room:
                self.hotel_instance.delete()

        def test_token_authentication(self):
            # rest_framework APIClient logging in
            self.client = APIClient()

            self.client.force_authenticate(user=self.superuser, token=self.superuser_token)

        def test_rest_user(self):
            # superuser logging in
            self.client.login(**self.creds_user)

            # GET
            resp_get = self.client.get(url)
            self.assertEqual(resp_get.status_code, status.HTTP_200_OK)

            # POST
            resp_post = self.client.post(url, data=self.request_data)
            self.assertEqual(resp_post.status_code, status.HTTP_403_FORBIDDEN)

            # PUT
            created = cls_model.objects.create(**self.request_data)
            url_to_created = f'{url}{created.id}/'
            self.request_data[attr] = attr_value
            resp_put = self.client.put(url_to_created, format='multipart', data=self.request_data)
            self.assertEqual(resp_put.status_code, status.HTTP_403_FORBIDDEN)

            # DELETE
            resp_delete = self.client.delete(url_to_created)
            self.assertEqual(resp_delete.status_code, status.HTTP_403_FORBIDDEN)

            created.delete()

            # user logging out
            self.client.logout()

    return ViewSetTests

hotel_data = {
    "company": "company",
    "name": "name",
    "star_rating": 4,
    "rooms_quantity": 10,
    "check_in": "15:00",
    "check_out": "12:00",
    "country": "country",
    "city": "city",
    "street": "city",
    "building": "1",
    "latitude": 59.842725,
    "longitude": 30.31841
}

room_data = {
    "hotel": None,
    "type": "standart",
    "code": "9-909",
    "price": 1000,
    "capacity": 2,
    "double_bed": 0,
    "single_bed": 2
}

AmenityViewTests = create_viewset_tests('/rest/amenity/', Amenity, {'title': 'title'}, 'title', 'new_title')
HotelViewTests = create_viewset_tests('/rest/hotel/', Hotel, hotel_data, 'description', 'description')
RoomViewTests = create_viewset_tests('/rest/room/', Room, room_data, 'area', 25, hotel=hotel_data)
