"""File with consts."""
from django.utils.translation import gettext_lazy as _

# models fields
CHARS_DEFAULT = 40
PHONE_LENGTH = 11
CHECK_IN_OUT_LEN = 5
CHAR_BUILD_LENGTH = 5
DECIMAL_PLACES = 2
DECIMAL_MAX_DIGITS = 10
STATUS_LENGTH = 10

# values
LATITUDE = 90
LONGITUDE = 180

# API methods
SAFE_METHODS = 'GET', 'HEAD', 'OPTIONS', 'PATCH'
UNSAFE_METHODS = 'POST', 'PUT', 'DELETE'


# choice fields
ROOM_TYPE_CHOICES = (
    ('Standart', _('Standart')),
    ('Superior', _('Superior')),
    ('Suite', _('Suite')),
    ('Family room', _('Family room')),
    ('Deluxe', _('Deluxe')),
    ('Apartments', _('Apartments')),
    ('Studio', _('Studio')),
    ('Duplex', _('Duplex')),
    ('Business room', _('Business room')),
    ('Royal suite', _('Royal suite')),
)

BOOKING_STATUSES = (
    ('Booked', 'Booked'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled')
)

PAYMENT_CHOICES = (
    ('cash', _('cash')),
    ('credit card', _('credit card')),
)

RATING_CHOICES = (
    (5, '5 stars'),
    (4, '4 stars'),
    (3, '3 stars'),
    (2, '2 stars'),
    (1, '1 or less stars')
)

# templates
MAIN_PAGE = 'index.html'
FIND_PAGE = 'find.html'
ACCOUNT_PAGE = 'account_page.html'
ROOMS_PAGE = 'rooms.html'
REGISTER_PAGE = 'register.html'
LOG_IN_PAGE = 'login.html'
BOOKING_PAGE = 'book.html'
CLIENT_BOOKINGS = 'client_bookings.html'
FAIL_PAGE = 'fail.html'
SUCCESS_PAGE = 'success.html'


BOOST_URL = 'https://boostbank.ru/rest/payment/'
BOOST_HEADERS = {'Authorization': 'Token ca936568a46528fec0657c5d0c9a77050c9f2d24'}
BOOST_REDIRECT = 'https://boostbank.ru/payment/{id}'
BOOST_ACCOUNT = 'ab0f0ccf-1e19-4e35-a84b-addc3753f4c0'
STATIC_THANKS = 'http://10.82.193.174:8000/success'
BOOST_CALLBACK_URL = 'http://10.82.193.174:8000/rest/Booking/{id}/'
BOOST_CALLBACK_HEADERS = {'Authorization': 'Token 6a399c43869cd6f7028a3cc498416431ad9a45c8'}
