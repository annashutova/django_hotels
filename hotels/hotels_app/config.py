"""File with consts."""
from django.utils.translation import gettext_lazy as _

# models fields
CHARS_DEFAULT = 40
PHONE_LENGTH = 14
CHECK_IN_OUT_LEN = 5
CHAR_BUILD_LENGTH = 5
DECIMAL_PLACES = 2
DECIMAL_MAX_DIGITS = 10

# values
LATITUDE = 90
LONGITUDE = 180

# API methods
SAFE_METHODS = 'GET', 'HEAD', 'OPTIONS', 'PATCH'
UNSAFE_METHODS = 'POST', 'PUT', 'DELETE'


# choice fields
CITIZENSHIP_CHOICES = (
('afghanistan', _('Afghanistan')),
('albania', _('Albania')),
('algeria', _('Algeria')),
)

ROOM_TYPE_CHOICES = (
    ('standart', _('Standart')),
    ('superior', _('Superior')),
    ('suite', _('Suite')),
    ('family_room', _('Family room')),
    ('deluxe', _('Deluxe')),
    ('apartments', _('Apartments')),
    ('studio', _('Studio')),
    ('duplex', _('Duplex')),
    ('business_room', _('Business room')),
    ('royal_suite', _('Royal suite')),
)

PAYMENT_CHOICES = (
    ('cash', _('cash')),
    ('credit_card', _('credit card')),
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
