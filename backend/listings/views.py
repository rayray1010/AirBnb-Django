import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Listing
from .serializer import ListingSerializer, CreateListingSerializer, RetriveListingSerializer
from imgurpython import ImgurClient
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from .filters.retriveListsFilter import ListingFilter
from reservations.models import Reservation
from reservations.serializer import ReservationSerializer
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from django.db.models import Q


class ListingListCreaetView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = CreateListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ListingFilter

    def get_queryset(self):
        # 获取查询参数中的startDate和endDate
        start_date = self.request.query_params.get('startDate')
        end_date = self.request.query_params.get('endDate')
        if not start_date or not end_date:
            return super().get_queryset()
        # 将查询参数转换为日期对象
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # 使用Q对象构建筛选条件
        reservations_in_range = Q(
            start_date__lte=end_date, end_date__gte=start_date)

        # 获取在指定日期范围内已被预订的Listing的ID
        reserved_listing_ids = Reservation.objects.filter(
            reservations_in_range).values_list('listing_id', flat=True)

        # 使用exclude()排除已被预订的Listing
        queryset = Listing.objects.exclude(id__in=reserved_listing_ids)

        return queryset

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        image = self.request.data.get('image')

        if not image:
            raise APIException(
                "image is required!", code=400)
        image_url = get_imgur_url(image)
        serializer.save(userId=self.request.user, imageSrc=image_url)


class AddToFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            listing = Listing.objects.get(id=pk)
        except Listing.DoesNotExist:
            return Response({"error": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)
        user = request.user
        if user.favorites.filter(id=pk).exists():
            user.favorites.remove(listing)
            return Response({"message": "Listing removed from favorites"}, status=status.HTTP_202_ACCEPTED)
        else:
            user.favorites.add(listing)
            return Response({"message": "Listing added to favorites"}, status=status.HTTP_201_CREATED)
    # delete a listing from favorites


# list all listings or retrive a single listing by id


class RetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = RetriveListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.owner:
            raise APIException(
                "You are not the owner of this listing!", code=400)
        image = self.request.data.get('image')
        if image:
            image_url = get_imgur_url(image)
            serializer.save(imageSrc=image_url)
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.owner:
            raise APIException(
                "You are not the owner of this listing!", code=400)
        return super().perform_destroy(instance)


def get_imgur_url(image):
    image_name = default_storage.save(image.name, image)
    client_id = "a5220230d536e8e"
    client_secret = "3d5118bfcf260b9f801d28b53b12fe572b93bb80"
    client = ImgurClient(client_id, client_secret)
    image_url = client.upload_from_path(
        settings.MEDIA_ROOT+'/'+image_name, anon=True)['link']
    default_storage.delete(image_name)
    return image_url

# query reservations by listing_id


class ListingReservationView(generics.ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        listing_id = self.kwargs.get('listing_id')
        queryset = Reservation.objects.filter(listing_id=listing_id)
        return queryset


class ListingOwnerView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateListingSerializer

    def get_queryset(self):
        owner = self.request.user
        queryset = Listing.objects.filter(owner=owner)
        return queryset
