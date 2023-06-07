from .models import Amenity, Hotel, Room, Booking
from rest_framework.serializers import ModelSerializer


class AmenitySerializer(ModelSerializer):

    class Meta:
        model = Amenity
        fields = ('id', 'title')


class HotelSerializer(ModelSerializer):

    class Meta:
        model = Hotel
        fields = (
            'id', 'company','name', 'star_rating',
            'country', 'state', 'city', 'street', 'building',
            'latitude', 'longitude'
        )

class BookingSerializer(ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            'id',
        )


class RoomSerializer(ModelSerializer):
    hotel = HotelSerializer()

    def create(self, validated_data):
        hotel = Hotel.objects.create(
            company=validated_data['hotel']['company'],
            name=validated_data['hotel']['name'],
            star_rating=validated_data['hotel']['star_rating'],
            country=validated_data['hotel']['country'],
            state=validated_data['hotel']['state'],
            city=validated_data['hotel']['city'],
            street=validated_data['hotel']['street'],
            building=validated_data['hotel']['building'],
            latitude=validated_data['hotel']['latitude'],
            longitude=validated_data['hotel']['longitude'],
        )
        return Room.objects.create(
            hotel=hotel,
            type=validated_data['type'],
            code=validated_data['code'],
            price=validated_data['price'],
            capacity=validated_data['capacity'],
            double_bed=validated_data['double_bed'],
            single_bed=validated_data['single_bed'],
            safe=validated_data['safe'],
            tv=validated_data['tv'],
            soundproofing=validated_data['soundproofing'],
            telephone=validated_data['telephone'],
            heating=validated_data['heating'],
            wardrobe=validated_data['wardrobe'],
            shower=validated_data['shower'],
            minibar=validated_data['minibar'],
            air_conditioning=validated_data['air_conditioning'],
            bath=validated_data['bath'],
            desk=validated_data['desk']
        )

    class Meta:
        model = Room
        fields = (
            'id', 'hotel', 'type', 'code', 'price',
            'capacity', 'double_bed', 'single_bed',
            'safe', 'tv', 'soundproofing', 'minibar',
            'telephone', 'heating', 'wardrobe', 'shower',
            'air_conditioning', 'bath', 'desk'
        )
