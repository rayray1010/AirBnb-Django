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
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Reservation.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def perform_destroy(self, instance):
        print(self.request.user)
        print(instance.user_id.id)
        if self.request.user.id != instance.user_id.id and self.request.user.id != instance.listing_id.owner_id:
            raise APIException(
                "You are not authorized to delete this reservation", code=400)
        return super().perform_destroy(instance)


class ListReservationFromUserView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Reservation.objects.filter(user_id=request.user)
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)


class ReservationByListingIdView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Reservation.objects.filter(listing_id=self.kwargs['pk'])
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)


class ReservationCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = CreateReservationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Reservation.objects.all()
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        self.validate_reservation(serializer.validated_data)
        serializer.save(userId=self.request.user)

    def validate_reservation(self, validated_data):
        listing = validated_data['listing_id']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        total_price = validated_data['total_price']

        listing = get_object_or_404(Listing, id=listing.id)
        listing_price = listing.price

        self.check_total_price(listing_price, start_date,
                               end_date, total_price)
        self.check_overlapping_reservations(listing, start_date, end_date)

    def check_total_price(self, listing_price, start_date, end_date, total_price):
        days = (end_date - start_date).days
        estimated_price = listing_price * days
        if estimated_price != total_price:
            raise APIException(
                f"totalPrice should be {estimated_price}", code=400)

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


class ReservationByListingOwnerView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Reservation.objects.filter(
            listing_id__owner_id=self.request.user)
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)
