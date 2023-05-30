from rest_framework import viewsets, permissions, status as status_codes
from .models import Amenity, Hotel, Room, Booking
from . import serializers, config, forms
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date, datetime
from django.db.models import F, Q


class Permission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in config.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in config.UNSAFE_METHODS:
            return bool(request.user and request.user.is_superuser)
        return False


def query_from_request(request, serializer=None) -> dict:
    if serializer:
        query = {}
        for attr in serializer.Meta.fields:
            attr_value = request.GET.get(attr, '')
            if attr_value:
                query[attr] = attr_value
        return query
    return request.GET


def create_viewset(model, serializer):
    class CustomViewSet(viewsets.ModelViewSet):
        serializer_class = serializer
        permission_classes = [Permission]

        def get_queryset(self):
            instances = model.objects.all()
            query = query_from_request(self.request, serializer)
            if query:
                instances = instances.filter(**query)
            return instances
        
        @action(detail=False, methods=['delete'])
        def delete(self, request):
            query = query_from_request(request, serializer)
            if query:
                instances = model.objects.filter(**query)
                objects_num = len(instances)
                if not objects_num:
                    msg = f'DELETE query {query} did not match any instances of {model.__name__}'
                    return Response(msg, status=status_codes.HTTP_404_NOT_FOUND)
                try:
                    instances.delete()
                except Exception as error:
                    return Response(error, status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
                if objects_num == 1:
                    ending = ''
                    status = status_codes.HTTP_204_NO_CONTENT
                else:
                    ending = 's'
                    status = status_codes.HTTP_200_OK
                msg = f'DELETED {objects_num} instance{ending} of {model.__name__}'
                return Response(msg, status=status)
            return Response('DELETE has got no query', status=status_codes.HTTP_400_BAD_REQUEST)

    return CustomViewSet


AmenityViewSet = create_viewset(Amenity, serializers.AmenitySerializer)
HotelViewSet = create_viewset(Hotel, serializers.HotelSerializer)
RoomViewSet = create_viewset(Room, serializers.RoomSerializer)

def validate_dates(check_in: str, check_out: str) -> tuple:
    # check_in = datetime.strptime(check_in, '%Y-%m-%d').date()
    # check_out = datetime.strptime(check_out, '%Y-%m-%d').date()
    if check_in < date.today():
        return (False, 'Check-in date cannot be in the past.')
    if check_out <= check_in:
        return (False, 'Check-out date cannot be before check in date.')
    return (True, '')


def main_page(request):
    form_errors = []
    if request.method == 'POST':
        form = forms.HotelFindForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data.get('check_in')
            check_out = form.cleaned_data.get('check_out')
            result, msg = validate_dates(check_in, check_out)
            if result:
                request.session['find_hotel'] = request.POST
                return redirect(reverse('find'))
            form_errors.append(msg)
    else:
        form = forms.HotelFindForm()
    
    return render(
        request,
        config.MAIN_PAGE,
        context={'form': form, 'errors': form_errors}
        )


def find_page(request):
    country = request.session['find_hotel'].get('country')
    city = request.session['find_hotel'].get('city')
    check_in = request.session['find_hotel'].get('check_in')
    check_out = request.session['find_hotel'].get('check_out')
    capacity = int(request.session['find_hotel'].get('capacity'))


    rooms = Room.objects.filter(
        hotel__country=country,
        hotel__city=city,
        capacity=capacity
    )

    all_bookings = {}
    hotels = set()
    for room in rooms:
        all_bookings[room] = Booking.objects.filter(room=room)
    print(all_bookings)
    print()
    print()

    for room_bookings in all_bookings:
        if not all_bookings[room_bookings]:
            print(room_bookings)
            continue
        all_bookings[room_bookings] = all_bookings[room_bookings].exclude(
            Q(check_in__range=(check_in, check_out)) | Q(check_out__range=(check_in, check_out))
            )
        if not all_bookings[room_bookings]:
            print(room_bookings)
            hotels.add(room_bookings.hotel)
    print(hotels)
    print(all_bookings)
    amenities = Amenity.objects.all()

    return render(request, config.FIND_PAGE, context={'amenities': amenities})
