from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from . import config
from django.conf.global_settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta, date


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Amenity(UUIDMixin):
    title = models.CharField(_('title'), max_length=config.CHARS_DEFAULT, unique=True)
    hotels = models.ManyToManyField('Hotel', verbose_name=_('hotels'), through='HotelAmenity')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'amenity'
        ordering = ['title']
        verbose_name = _('amenity')
        verbose_name_plural = _('amenities')


class Hotel(UUIDMixin):
    company = models.CharField(_('company'), max_length=config.CHARS_DEFAULT, blank=True, null=True)
    name = models.CharField(_('name'), max_length=config.CHARS_DEFAULT)
    star_rating = models.PositiveSmallIntegerField(
        verbose_name=_('star rating'),
        default=0,
        validators=[MaxValueValidator(5)],
    )
    country = models.CharField(_('country'), max_length=config.CHARS_DEFAULT)
    state = models.CharField(_('state'), max_length=config.CHARS_DEFAULT, blank=True, null=True)
    city = models.CharField(_('city'), max_length=config.CHARS_DEFAULT)
    street = models.CharField(_('street'), max_length=config.CHARS_DEFAULT)
    building = models.CharField(_('building'), max_length=config.CHAR_BUILD_LENGTH)
    latitude = models.FloatField(
        verbose_name=_('latitude'),
        validators=[MinValueValidator(-config.LATITUDE), MaxValueValidator(config.LATITUDE)],
    )
    longitude = models.FloatField(
        verbose_name=_('longitude'),
        validators=[MinValueValidator(-config.LONGITUDE), MaxValueValidator(config.LONGITUDE)],
    )
    amenities = models.ManyToManyField(Amenity, verbose_name=_('amenities'), through='HotelAmenity')

    def __str__(self):
        return f'{self.name}, {self.country}'

    class Meta:
        indexes = [models.Index(fields=['name'], name='hotel_name_idx')]
        constraints = [
            models.CheckConstraint(
                check=models.Q(star_rating__gte=0) & models.Q(star_rating__lte=5),
                name='star_rate_check',
            ),
            models.CheckConstraint(
                check=models.Q(latitude__gte=-config.LATITUDE) & models.Q(latitude__lte=config.LATITUDE),
                name='latitude_check',
            ),
            models.CheckConstraint(
                check=models.Q(longitude__gte=-config.LONGITUDE) & models.Q(longitude__lte=config.LONGITUDE),
                name='longitude_check',
            ),
        ]
        ordering = ['name']
        db_table = 'hotel'
        verbose_name = _('hotel')
        verbose_name_plural = _('hotels')


class HotelAmenity(UUIDMixin):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        db_table = 'hotel_amenity'
        unique_together = (('hotel', 'amenity'),)
        verbose_name = _('hotel amenity')
        verbose_name_plural = _('hotel amenities')


class Room(UUIDMixin):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    type = models.CharField(_('type'), max_length=config.CHARS_DEFAULT, choices=config.ROOM_TYPE_CHOICES)
    code = models.CharField(_('code'), max_length=config.CHARS_DEFAULT)
    price = models.DecimalField(
        verbose_name=_('price'),
        max_digits=config.DECIMAL_MAX_DIGITS,
        decimal_places=config.DECIMAL_PLACES,
        validators=[MinValueValidator(1)],
    )
    capacity = models.PositiveSmallIntegerField(_('capacity'))
    double_bed = models.PositiveSmallIntegerField(_('double bed'))
    single_bed = models.PositiveSmallIntegerField(_('single bed'))
    safe = models.BooleanField(_('safe'), default=False, blank=True, null=True)
    tv = models.BooleanField(_('tv'), default=False, blank=True, null=True)
    soundproofing = models.BooleanField(_('soundproofing'), default=False, blank=True, null=True)
    telephone = models.BooleanField(_('telephone'), default=False, blank=True, null=True)
    heating = models.BooleanField(_('heating'), default=False, blank=True, null=True)
    wardrobe = models.BooleanField(_('wardrobe'), default=False, blank=True, null=True)
    shower = models.BooleanField(_('shower'), default=False, blank=True, null=True)
    minibar = models.BooleanField(_('minibar'), default=False, blank=True, null=True)
    air_conditioning = models.BooleanField(_('air conditioning'), default=False, blank=True, null=True)
    bath = models.BooleanField(_('bath'), default=False, blank=True, null=True)
    desk = models.BooleanField(_('desk'), default=False, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.capacity > self.double_bed * 2 + self.single_bed:
            raise ValidationError(
                {'capacity': _('Capacity may not exeed number of beds.')},
                params={'capacity': self.capacity},
            )

    def __str__(self):
        return f'{self.hotel}, {self.type}, {self.code}'

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='room_price_check'),
            models.CheckConstraint(check=models.Q(capacity__gt=0), name='capacity_check'),
            models.CheckConstraint(check=models.Q(double_bed__gte=0), name='double_bed_check'),
            models.CheckConstraint(check=models.Q(single_bed__gte=0), name='single_bed_check'),
        ]
        db_table = 'room'
        unique_together = (('hotel', 'code'),)
        verbose_name = _('room')
        verbose_name_plural = _('rooms')


def validate_birth(date_of_birth: date):
    if date_of_birth > date.today():
        raise ValidationError(
            {'date_of_birth': _('Date of birth is greater than current date.')},
            params={'date_of_birth': date_of_birth},
        )


class Client(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(verbose_name=_('phone'), max_length=config.PHONE_LENGTH)
    date_of_birth = models.DateField(blank=True, null=True, validators=[validate_birth])

    def __str__(self):
        return self.user.username

    def clean_phone(self):
        number = self.cleaned_data.get('phone')
        cleaned_value = ''.join(filter(str.isdigit, number))
        if len(cleaned_value) != config.PHONE_LENGTH or not cleaned_value.startswith(('7', '8')):
            raise ValidationError(
                'Invalid phone number!',
                params={"phone": number},
            )

    class Meta:
        db_table = 'client'
        verbose_name = _('client')
        verbose_name_plural = _('clients')


def get_checkout_date():
    return date.today() + timedelta(1.0)


class Booking(UUIDMixin):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    check_in = models.DateField(_('check_in'), default=date.today)
    check_out = models.DateField(_('check_out'), default=get_checkout_date)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=config.STATUS_LENGTH,
        choices=config.BOOKING_STATUSES,
        default='Booked',
        blank=True,
        null=False,
    )
    price = models.DecimalField(
        verbose_name=_('price'),
        max_digits=config.DECIMAL_MAX_DIGITS,
        decimal_places=config.DECIMAL_PLACES,
        validators=[MinValueValidator(1)],
    )
    created = models.DateTimeField(_('created'), auto_now_add=True, editable=False)

    class Meta:
        unique_together = (('check_in', 'check_out', 'room'),)
        ordering = ['-check_in', '-check_out']
        db_table = 'booking'
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')

    def validate_booking(self) -> bool:
        try:
            room_bookings = Booking.objects.all().filter(room__id=self.room.id)
        except ObjectDoesNotExist:
            return False
        for booking in room_bookings:
            if booking.check_in < self.check_in < booking.check_out:
                return False
            if booking.check_in < self.check_out < booking.check_out:
                return False
        return True

    def clean(self):
        super().clean()
        if self.check_out <= self.check_in:
            raise ValidationError(
                {'check_in': _('Check in date must be less than check_out.')},
                params={'check_in': self.check_in, 'check_out': self.check_out},
            )
        if not self.validate_booking():
            raise ValidationError(
                'Room is already booked during choosen dates.',
                params={'check_in': self.check_in, 'check_out': self.check_out},
            )

    def __str__(self):
        return f'{self.check_in}-{self.check_out}, {self.room}'
