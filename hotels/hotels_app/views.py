from rest_framework import viewsets, permissions, status as status_codes
from .models import Amenity, Hotel, Room, Booking, HotelAmenity, Client
from . import serializers, config, forms
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.urls import reverse
from django.db import models, transaction
from django.contrib.auth import password_validation, hashers, models as auth_models, authenticate, login, logout, decorators
from . import validators
from datetime import date, datetime
import requests as rq


def query_from_request(request, cls_serializer=None) -> dict:
    if cls_serializer:
        query = {}
        for attr in cls_serializer.Meta.fields:
            request.GET.get(attr, '')
        return query


def create_viewset(cls_model: models.Model, serializer, permission, order_field):
    class_name = f"{cls_model.__name__}ViewSet"
    doc = f"API endpoint that allows users to be viewed or edited for {cls_model.__name__}"
    CustomViewSet = type(class_name, (viewsets.ModelViewSet,), {
        "__doc__": doc,
        "serializer_class": serializer,
        "queryset": cls_model.objects.all().order_by(order_field),
        "permission classes": [permission],
        "get_queryset": lambda self, *args, **kwargs: cls_model.objects.filter(**query_from_request(self.request, serializer)).order_by(order_field)}
    )

    return CustomViewSet


AmenityViewSet = create_viewset(
    Amenity,
    serializers.AmenitySerializer,
    permissions.BasePermission,
    'id'
    )
HotelViewSet = create_viewset(
    Hotel,
    serializers.HotelSerializer,
    permissions.BasePermission,
    'id'
    )
RoomViewSet = create_viewset(
    Room,
    serializers.RoomSerializer,
    permissions.BasePermission,
    'id'
    )
BookingViewSet = create_viewset(
    Booking,
    serializers.BookingSerializer,
    permissions.BasePermission,
    'id'
    )


@decorators.login_required
def main_page(request):
    form_errors = []
    if request.method == 'POST':
        form = forms.HotelFindForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data.get('check_in')
            check_out = form.cleaned_data.get('check_out')
            try:
                validators.validate_dates(check_in, check_out)
            except Exception as error:
                form_errors.append(error.message)
            else:
                request.session['find_hotel'] = request.POST
                return redirect(reverse('find'))
    else:
        form = forms.HotelFindForm()
    
    return render(
        request,
        config.MAIN_PAGE,
        context={'form': form, 'errors': form_errors}
        )


@decorators.login_required
def find_page(request):
    country = request.session['find_hotel'].get('country')
    city = request.session['find_hotel'].get('city')
    check_in = request.session['find_hotel'].get('check_in')
    check_out = request.session['find_hotel'].get('check_out')
    capacity = request.session['find_hotel'].get('capacity')

    amenities = [amenity.title for amenity in Amenity.objects.all()]

    hotel_query = {}
    room_query = {}
    query = request.GET
    all_ratings = ['0', '1', '2', '3', '4', '5']
    star_ratings = []
    for key in query:
        if key in all_ratings:
            star_ratings.append(key)
        elif key in amenities:
            hotel_query[key] = True
        else:
            room_query[key] = True
    request.session['room_query'] = room_query

    rooms = Room.objects.filter(
        hotel__country=country,
        hotel__city=city,
        capacity=capacity,
        **room_query
    )

    all_bookings = {}
    hotels = set()
    for room in rooms:
        all_bookings[room] = Booking.objects.filter(room=room)

    for room in all_bookings:
        all_bookings[room] = all_bookings[room].exclude(
            models.Q(check_in__gte=check_out )| models.Q(check_out__lte=check_in)
            )
        if not all_bookings[room]:
            hotels.add(room.hotel)

    final_hotels = []
    for hotel in hotels:
        if star_ratings:
            if str(hotel.star_rating) not in star_ratings:
                continue
        hotel_amenities = [record.amenity.title for record in HotelAmenity.objects.filter(hotel=hotel)]
        for key in hotel_query:
            if key not in hotel_amenities:
                break
        else:
            price_max = Room.objects.filter(hotel=hotel).aggregate(models.Max('price'))['price__max']
            price_min = Room.objects.filter(hotel=hotel).aggregate(models.Min('price'))['price__min']
            hotel_data = [hotel, price_min, price_max]
            final_hotels.append(hotel_data) if hotel_data not in final_hotels else None


    amenities = Amenity.objects.all()
    
    context = {
        'amenities': amenities,
        'city': city,
        'hotels': final_hotels
    }

    return render(request, config.FIND_PAGE, context=context)


@decorators.login_required
def rooms_page(request):
    check_in = request.session['find_hotel'].get('check_in')
    check_out = request.session['find_hotel'].get('check_out')
    hotel = Hotel.objects.get(id=request.GET.get('id'))
    rooms = Room.objects.filter(
        hotel=hotel,
        capacity=request.session['find_hotel'].get('capacity'),
        **request.session['room_query']
        )
    nights = (datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days
    all_bookings = {}
    all_rooms = []
    for room in rooms:
        all_bookings[room] = Booking.objects.filter(room=room)

    for room in all_bookings:
        all_bookings[room] = all_bookings[room].exclude(
            models.Q(check_in__gte=check_out )| models.Q(check_out__lte=check_in)
            )
        if not all_bookings[room]:
            all_rooms.append([room, room.price * nights])

    context = {
        'rooms': all_rooms,
        'hotel': hotel.name,
        'nights': f'{nights} night' if nights == 1 else f'{nights} nights'
    }

    return render(request, config.ROOMS_PAGE, context=context)


@decorators.login_required
def booking_page(request):
    check_in = request.session['find_hotel'].get('check_in')
    check_out = request.session['find_hotel'].get('check_out')
    room = Room.objects.get(id=request.GET.get('id'))
    check_in = datetime.strptime(check_in, '%Y-%m-%d')
    check_out = datetime.strptime(check_out, '%Y-%m-%d')
    nights = check_out - check_in
    price = room.price * nights.days
    request.session['room_booking'] = {
        'room_id': str(room.id),
        'price': str(price)
    }
    context = {
        'room': room,
        'check_in': check_in.strftime('%d %b, %Y'),
        'check_out': check_out.strftime('%d %b, %Y'),
        'room_price': price
    }
    return render(request, config.BOOKING_PAGE, context=context)


@decorators.login_required
def booking_confirmation(request):
    if request.method == 'POST':
        check_in = request.session['find_hotel'].get('check_in')
        check_out = request.session['find_hotel'].get('check_out')
        room = Room.objects.get(id=request.session['room_booking'].get('room_id'))
        price = request.session['room_booking'].get('price')
        if Booking.objects.filter(
            check_in=check_in,
            check_out=check_out,
            room=room
            ).exists():
            return redirect('fail')
        client = Client.objects.get(user=request.user)
        booking = Booking.objects.create(
            client=client,
            check_in=check_in,
            check_out=check_out,
            room=room,
            status='Booked',
            price=price
        )
        response = rq.post(
            url=config.BOOST_URL,
            headers=config.BOOST_HEADERS,
            json={
                'recipient': config.BOOST_ACCOUNT,
                'amount': booking.price,
                'callback':
                    {
                       'redirect': config.STATIC_THANKS,
                        'url': config.BOOST_CALLBACK_URL.format(id=booking.id),
                        'headers': config.BOOST_CALLBACK_HEADERS
                    }
                }
            )
        id = response.json().get('id')
        return redirect(config.BOOST_REDIRECT.format(id=id))
    return render(request, config.FAIL_PAGE)


@decorators.login_required
def failed_booking(request):
    return render(request, config.FAIL_PAGE)


@decorators.login_required
def successful_booking(request):
    return render(request, config.SUCCESS_PAGE)


def create_bookings_view(period: str):
    @decorators.login_required
    def view(request):
        user = request.user
        client = Client.objects.get(user=user)
        params = {
            'client': client,
            f'check_out__{period}': date.today()
        }
        bookings = Booking.objects.filter(**params).order_by('check_in')
        all_bookings = []
        for booking in bookings:
            all_bookings.append([booking, booking.check_in.strftime('%d %b, %Y'), booking.check_out.strftime('%d %b, %Y')])
        return render(request, config.CLIENT_BOOKINGS, {'bookings': all_bookings})
    return view


current_bookings = create_bookings_view('gte')
past_bookings = create_bookings_view('lt')


@decorators.login_required
def account(request):
    user = request.user
    client = Client.objects.get(user=user)
    form_errors = []
    if request.method == 'POST':
        form = forms.PersonalData(
            data=request.POST,
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': client.phone,
                'date_of_birth': client.date_of_birth,
            }
            )
        if form.is_valid():
            b_date = form.cleaned_data.get('date_of_birth')
            phone = form.cleaned_data.get('phone')
            f_name = form.cleaned_data.get('first_name')
            l_name = form.cleaned_data.get('last_name')
            # validate date_of_birth
            try:
                validators.validate_birth(b_date)
            except Exception as error:
                form_errors.append(error)
            else:
                client.date_of_birth = b_date
            # validate phone number
            try:
                validators.validate_phone(phone)
            except Exception:
                form_errors.append(error)
            else:
                client.phone = phone
            # validate names
            try:
                validators.validate_name(f_name)
                validators.validate_name(l_name)
            except Exception as error:
                form_errors.append(error)
            else:
                user.first_name = f_name
                user.last_name = l_name
            if not form_errors:
                client.save()
                user.save()
    else:
        form = forms.PersonalData(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': client.phone,
                'date_of_birth': client.date_of_birth,
            }
        )
    client_data = {
        'Username': user.username,
        'First name': user.first_name,
        'Last name': user.last_name,
        'Email': user.email,
        'Phone number': client.phone,
        'Date of birth': client.date_of_birth
    }

    context = {
        'client_data': client_data,
        'form': form,
        'errors': form_errors,
    }
    return render(request, config.ACCOUNT_PAGE, context=context)


def register(request):
    form_errors = []
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            b_date = form.cleaned_data.get('date_of_birth')
            phone = form.cleaned_data.get('phone')
            f_name = form.cleaned_data.get('first_name')
            l_name = form.cleaned_data.get('last_name')
            print(phone)
            # validate username
            try:
                validators.validate_new_username(username)
            except Exception as error:
                form_errors.append(error.message)
            # validate email
            try:
                validate_email(email)
            except Exception as error:
                form_errors.append(error.message)
            # validate date_of_birth
            try:
                validators.validate_birth(b_date)
            except Exception as error:
                form_errors.append(error.message)
            # validate names
            try:
                validators.validate_name(f_name)
                validators.validate_name(l_name)
            except Exception as error:
                form_errors.append(error.message)
            # validate phone number
            try:
                validators.validate_phone(phone)
            except Exception as error:
                form_errors.append(error.message)
            # validate passwords
            try:
                password_validation.validate_password(password1)
            except Exception as error:
                form_errors.append(error)
            try:
                validators.validate_passwords(password1, password2)
            except Exception as error:
                form_errors.append(error.message)
            
            if not form_errors:
                with transaction.atomic():
                    user = auth_models.User.objects.create(
                        username=username,
                        email=email,
                        first_name=f_name,
                        last_name=l_name,
                        password=hashers.make_password(password1)
                    )
                    Client.objects.create(
                        user=user,
                        date_of_birth=b_date,
                        phone=phone,
                    )
                return redirect(reverse('main page'))

    else:
        form = forms.RegistrationForm()
    return render(request, config.REGISTER_PAGE, {'form': form, 'errors': form_errors})


def login_view(request):
    error = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('main page'))
            else:
                error = 'Username or password is invalid. Try again.'
    else:
        form = forms.LoginForm()
    return render(request, config.LOG_IN_PAGE, {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect(reverse('register'))
