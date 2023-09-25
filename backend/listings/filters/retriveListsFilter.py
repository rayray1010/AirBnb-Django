from django_filters import rest_framework as filters
from ..models import Listing


class ListingFilter(filters.FilterSet):
    userId = filters.NumberFilter(field_name='owner')
    guestCount = filters.NumberFilter(field_name='guest_count')
    bathroomCount = filters.NumberFilter(field_name='bathroom_count')
    roomCount = filters.NumberFilter(field_name='room_count')
    locationValue = filters.CharFilter(field_name='location_value')

    class Meta:
        model = Listing
        fields = ["title", 'category', 'price']
