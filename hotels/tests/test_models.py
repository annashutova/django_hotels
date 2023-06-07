from django.test import TestCase
from hotels_app import models, config
from django.db.utils import DataError, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from random import sample
from string import ascii_letters
from datetime import timedelta, date


def create_simple_model_tests(cls_model, attrs, failing_attrs):
    class ModelsTests(TestCase):

        def test_good_attrs(self):
            cls_model.objects.create(**attrs)

        def test_fail_attrs(self):
            with self.assertRaises(DataError):
                cls_model.objects.create(**failing_attrs)

    return ModelsTests

normal_name = ''.join(sample(ascii_letters, config.CHARS_DEFAULT - 1))
failing_name = ''.join(sample(ascii_letters, config.CHARS_DEFAULT + 1))

hotel_good_attrs = {
    'name': normal_name,
    'star_rating': 2,
    'country': 'country',
    'city': 'city',
    'street': 'street',
    'building': '23',
    'latitude': 34,
    'longitude': 34
}
hotel_fail_attrs = {
    'name': failing_name,
    'star_rating': 2,
    'country': 'country',
    'city': 'city',
    'street': 'street',
    'building': '23',
    'latitude': 34,
    'longitude': 34
}


HotelModelTests = create_simple_model_tests(models.Hotel, hotel_good_attrs, hotel_fail_attrs)
AmenityModelTests = create_simple_model_tests(models.Amenity, {'title': normal_name}, {'title': failing_name})


class RoomModelTests(TestCase):

    def setUp(self) -> None:
        self.hotel = models.Hotel.objects.create(
            name='name',
            star_rating=2,
            country='country',
            city='city',
            street='street',
            building='76',
            latitude=54,
            longitude=54,
        )

    def test_good_attrs(self):
        room_atttrs = {
            'hotel': self.hotel,
            'type': 'Standart',
            'code': '909',
            'price': 1000,
            'capacity': 2,
            'double_bed': 1,
            'single_bed': 0,
        }
        room = models.Room.objects.create(**room_atttrs)
        self.assertEqual(room.type, room_atttrs['type'])
        self.assertEqual(room.code, room_atttrs['code'])
        self.assertEqual(room.price, room_atttrs['price'])
        self.assertEqual(room.capacity, room_atttrs['capacity'])
        self.assertEqual(room.double_bed, room_atttrs['double_bed'])
        self.assertEqual(room.single_bed, room_atttrs['single_bed'])
        
    def test_fail_attrs(self):
        room_atttrs = {
            'hotel': self.hotel,
            'type': 'Standart',
            'code': '909',
            'price': 1000,
            'capacity': 0,
            'double_bed': 1,
            'single_bed': 0,
        }
        with self.assertRaises(IntegrityError):
            models.Room.objects.create(**room_atttrs)


class ClientModelTests(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
                username='test',
                first_name='test',
                last_name='test',
                email='test@mail.ru',
                password='test'
            )

    def test_good_attrs(self):
        client_attrs = {
            'user': self.user,
            'phone': '79143249952'
        }
        client = models.Client.objects.create(**client_attrs)
        self.assertEqual(client.user, self.user)
        self.assertEqual(client.phone, client_attrs['phone'])

    def test_fail_attrs(self):
        client_attrs = {
            'user': self.user,
            'phone': '991432566560909'
        }
        with self.assertRaises(ValidationError):
            client = models.Client(**client_attrs)
            client.full_clean()


class BookingModelTests(TestCase):

    def setUp(self) -> None:
        self.hotel = models.Hotel.objects.create(
            name='name',
            star_rating=2,
            country='country',
            city='city',
            street='street',
            building='76',
            latitude=54,
            longitude=54,
        )
        self.user = User.objects.create_user(
                username='test',
                first_name='test',
                last_name='test',
                email='test@mail.ru',
                password='test'
            )
        self.client = models.Client.objects.create(
            user=self.user,
            phone='79143249952'
        )
        self.room = models.Room.objects.create(
            hotel=self.hotel,
            type='Standart',
            code='909',
            price=1000,
            capacity=2,
            double_bed=1,
            single_bed=0,
        )

    def test_good_attrs(self):
        booking_attrs = {
            'client': self.client,
            'room': self.room,
            'check_in': date.today() + timedelta(days=1),
            'check_out': date.today() + timedelta(days=2),
            'status': 'Booked',
            'price': 1000
        }
        booking = models.Booking.objects.create(**booking_attrs)
        self.assertEqual(booking.check_in, booking_attrs['check_in'])
        self.assertEqual(booking.check_out, booking_attrs['check_out'])
        self.assertEqual(booking.room, booking_attrs['room'])
        self.assertEqual(booking.status, booking_attrs['status'])
        self.assertEqual(booking.price, booking_attrs['price'])
        self.assertEqual(booking.client, booking_attrs['client'])

    def test_fail_attrs(self):
        booking_attrs = {
            'client': self.client,
            'room': self.room,
            'check_in': date.today() + timedelta(days=2),
            'check_out': date.today() + timedelta(days=1),
            'status': 'Booked',
            'price': 1000
        }
        with self.assertRaises(ValidationError):
            booking = models.Booking(**booking_attrs)
            booking.full_clean()
