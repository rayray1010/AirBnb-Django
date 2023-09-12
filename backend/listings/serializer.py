from datetime import datetime
from rest_framework import serializers

from .models import Listing
from users.models import CustomUser


class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Listing
        fields = "__all__"


class CreateListingSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    guestCount = serializers.IntegerField(source='guest_count')
    location = serializers.CharField(max_length=100, source='location_value')
    bathroomCount = serializers.IntegerField(source='bathroom_count')
    roomCount = serializers.IntegerField(source='room_count')
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=1000)
    price = serializers.IntegerField()

    class Meta:
        model = Listing
        fields = [
            "owner",
            "image_src",
            "guestCount",
            "bathroomCount",
            "roomCount",
            "title",
            "description",
            "price",
            "location",
            "category"
        ]


# class CreateListingRequetSerializer(serializers.Serializer):
#     owner = serializers.IntegerField(default=1, allow_null=True)
#     categories = serializers.CharField(max_length=100)
#     location = serializers.ListField()
#     image = serializers.FileField()
#     guestCount = serializers.IntegerField()
#     bathroomCount = serializers.IntegerField()
#     roomCount = serializers.IntegerField()
#     price = serializers.IntegerField()
#     title = serializers.CharField(max_length=50)
#     description = serializers.CharField(max_length=1000)

#     def create(self, validated_data):
#         owner = validated_data.pop("owner")
#         title = validated_data.pop("title")
#         image_src = validated_data.pop("image")
#         description = validated_data.pop("description")
#         price = validated_data.pop("price")
#         room_count = validated_data.pop("roomCount")
#         bathroom_count = validated_data.pop("bathroomCount")
#         guest_count = validated_data.pop("guestCount")
#         location_value = validated_data.pop("location")
#         category = validated_data.pop("categories")

#         owner = CustomUser.objects.get(id=owner)
#         return Listing.objects.create(title=title, image_src=image_src, description=description, price=price, room_count=room_count,
#                                       bathroom_count=bathroom_count, guest_count=guest_count, location_value=location_value, category=category, owner=owner)
