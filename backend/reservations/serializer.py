from rest_framework import serializers
from .models import Reservation
from listings.models import Listing
from users.models import CustomUser
from listings.serializer import CreateListingSerializer


class ReservationSerializer(serializers.ModelSerializer):
    listing = CreateListingSerializer(source='listing_id', read_only=True)
    listingId = serializers.PrimaryKeyRelatedField(
        source='listing_id', queryset=Listing.objects.all())
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')
    userId = serializers.PrimaryKeyRelatedField(
        source='user_id', queryset=CustomUser.objects.all())
    totalPrice = serializers.IntegerField(source='total_price')
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Reservation
        fields = ['id', 'listing', 'listingId', 'startDate', 'endDate',
                  'userId', 'totalPrice', 'createdAt']


class CreateReservationSerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')
    listingId = serializers.PrimaryKeyRelatedField(
        source='listing_id', queryset=Listing.objects.all())
    userId = serializers.PrimaryKeyRelatedField(
        source='user_id', queryset=CustomUser.objects.all(), required=False)
    totalPrice = serializers.IntegerField(source='total_price')

    class Meta:
        model = Reservation
        fields = ['startDate', 'endDate', 'listingId', 'userId', 'totalPrice']

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        reservation = Reservation(user_id=userId, **validated_data)
        reservation.save()
        return reservation
