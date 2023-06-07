from django.contrib import admin
from .models import Hotel, Amenity, Room, HotelAmenity, Client, Booking


class HotelAmenityInline(admin.TabularInline):
    model = HotelAmenity
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    model = Hotel
    inlines = (HotelAmenityInline,)
    list_filter = (
        'name',
        'company',
        'country',
        'star_rating',
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    model = Amenity
    list_filter = (
        'title',
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    model = Room
    list_filter = (
        'type',
        'capacity',
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    model = Booking
    list_filter = (
        'check_in',
        'check_out',
        'room',
    )
