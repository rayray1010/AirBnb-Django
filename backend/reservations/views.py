from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from .models import Reservation
from .serializer import CreateReservationSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from listings.models import Listing
# Create your views here.


class RetriveReservationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'


class ReservationCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = CreateReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        self.validate_reservation(serializer.validated_data)
        serializer.save(user_id=self.request.user)

    def validate_reservation(self, validated_data):
        listing_id = validated_data['listing_id']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        total_price = validated_data['total_price']

        listing = get_object_or_404(Listing, id=listing_id.id)
        listing_price = listing.price

        self.check_total_price(listing_price, start_date,
                               end_date, total_price)
        self.check_overlapping_reservations(listing_id, start_date, end_date)

    def check_total_price(self, listing_price, start_date, end_date, total_price):
        days = (end_date - start_date).days
        estimated_price = listing_price * days
        if estimated_price != total_price:
            raise APIException(
                "Estimated price is not equal to total price", code=400)

    def check_overlapping_reservations(self, listing_id, start_date, end_date):
        if end_date <= start_date:
            raise APIException(
                "End date must be greater than start date", code=400)

        overlapping_reservations = Reservation.objects.filter(
            listing_id=listing_id,
            start_date__lte=end_date,
            end_date__gt=start_date
        )
        if overlapping_reservations.exists():
            raise APIException(
                "Reservation overlaps with existing reservation", code=400)
