from .models import Amenity, Hotel, Room
from rest_framework.serializers import HyperlinkedModelSerializer


class AmenitySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Amenity
        fields = ('id', 'title')


class HotelSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Hotel
        fields = (
            'id', 'company','name', 'star_rating',
            'rooms_quantity', 'phone', 'check_in',
            'check_out', 'description', 'country',
            'state', 'city', 'street', 'building',
            'latitude', 'longitude'
        )


class RoomSerializer(HyperlinkedModelSerializer):
    #hotel = HotelSerializer(read_only=True)

    class Meta:
        model = Room
        fields = (
            'id', 'hotel', 'type', 'code', 'price',
            'capacity', 'double_bed', 'single_bed',
            'area', 'description', 'safe', 'tv', 'soundproofing',
            'telephone', 'heating', 'wardrobe', 'shower', 'minibar',
            'air_conditioning', 'bath', 'desk'
        )
