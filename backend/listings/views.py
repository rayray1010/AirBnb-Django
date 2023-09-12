import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Listing
from .serializer import ListingSerializer, CreateListingSerializer
from imgurpython import ImgurClient
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.exceptions import APIException
from users.models import CustomUser


class ListingListCreaetView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = CreateListingSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        image = self.request.data.get('image')

        if not image:
            raise APIException(
                "image is required!", code=400)
        image_url = get_imgur_url(image)
        # owner = CustomUser.objects.get()
        serializer.save(owner=self.request.user, image_src=image_url)
        # serializer.save(owner=self.request.user, image_src=image_url)
    # def perform_create(self, serializer):
    #     image = self.request.data.get('image')
    #     if not image:
    #         raise APIException(
    #             "image is required!", code=400)
    #     image_url = get_imgur_url(image)
    #     serializer.save(owner=self.request.user, image_src=image_url)


class AddToFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            listing = Listing.objects.get(id=pk)
        except Listing.DoesNotExist:
            return Response({"error": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)
        user = request.user
        user.favorites.add(listing)
        return Response({"message": "Listing added to favorites"}, status=status.HTTP_201_CREATED)

# list all listings or retrive a single listing by id


class RetriveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        if 'image' in request.data:
            self.process_and_update_image()
        return super().patch(request, *args, **kwargs)

    def process_and_update_image(self):
        image = self.request.data['image']
        image_url = get_imgur_url(image)
        self.request.data['image_src'] = image_url


def get_imgur_url(image):
    image_name = default_storage.save(image.name, image)
    client_id = "a5220230d536e8e"
    client_secret = "3d5118bfcf260b9f801d28b53b12fe572b93bb80"
    client = ImgurClient(client_id, client_secret)
    image_url = client.upload_from_path(
        settings.MEDIA_ROOT+'/'+image_name, anon=True)['link']
    default_storage.delete(image_name)
    return image_url
