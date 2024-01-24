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
    id = serializers.IntegerField(read_only=True, source="pk")
    userId = serializers.PrimaryKeyRelatedField(
        source="owner", queryset=CustomUser.objects.all(), required=False
    )
    guestCount = serializers.IntegerField(source="guest_count")
    locationValue = serializers.CharField(max_length=100, source="location_value")
    bathroomCount = serializers.IntegerField(source="bathroom_count")
    roomCount = serializers.IntegerField(source="room_count")
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=1000)
    price = serializers.IntegerField()
    imageSrc = serializers.CharField(source="image_src", required=False)
    createdAt = serializers.DateTimeField(read_only=True, source="created_at")

    class Meta:
        model = Listing
        fields = [
            "id",
            "userId",
            "guestCount",
            "bathroomCount",
            "roomCount",
            "title",
            "description",
            "price",
            "locationValue",
            "category",
            "imageSrc",
            "createdAt",
        ]

    def create(self, validated_data):
        # 通過 validated_data 中的 userId 和 imageSrc 來創建模型實例
        image_src = validated_data.pop("imageSrc", None)
        owner = validated_data.pop("userId", None)
        listing = Listing.objects.create(
            owner=owner, image_src=image_src, **validated_data
        )
        return listing

    # patch method
    def update(self, instance, validated_data):
        # 通過 validated_data 中的 userId 和 imageSrc 來創建模型實例
        if "imageSrc" in validated_data:
            instance.image_src = validated_data.pop("imageSrc", None)
        if "userId" in validated_data:
            instance.owner = validated_data.pop("userId", None)
        instance.save()
        return instance


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


# class ListingOnerAndReservationSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True, source='pk')
#     userId = serializers.PrimaryKeyRelatedField(
#         source='owner', queryset=CustomUser.objects.all(), required=False)
#     guestCount = serializers.IntegerField(source='guest_count')
#     locationValue = serializers.CharField(
#         max_length=100, source='location_value')
#     bathroomCount = serializers.IntegerField(source='bathroom_count')
#     roomCount = serializers.IntegerField(source='room_count')
#     title = serializers.CharField(max_length=50)
#     description = serializers.CharField(max_length=1000)
#     price = serializers.IntegerField()
#     imageSrc = serializers.CharField(source='image_src', required=False)
#     createdAt = serializers.DateTimeField(read_only=True, source='created_at')
#     reservations = serializers.PrimaryKeyRelatedField(
#         many=True, read_only=True, source='reservation_set')

#     class Meta:
#         model = Listing
#         fields = [
#             "id",
#             "userId",
#             "guestCount",
#             "bathroomCount",
#             "roomCount",
#             "title",
#             "description",
#             "price",
#             "locationValue",
#             "category",
#             "imageSrc",
#             "createdAt",
#             "reservations"
#         ]


class RetriveListingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source="pk")
    userId = serializers.PrimaryKeyRelatedField(
        source="owner", queryset=CustomUser.objects.all(), required=False
    )
    guestCount = serializers.IntegerField(source="guest_count")
    locationValue = serializers.CharField(max_length=100, source="location_value")
    bathroomCount = serializers.IntegerField(source="bathroom_count")
    roomCount = serializers.IntegerField(source="room_count")
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=1000)
    price = serializers.IntegerField()
    imageSrc = serializers.CharField(source="image_src", required=False)
    createdAt = serializers.DateTimeField(read_only=True, source="created_at")
    ownerName = serializers.CharField(source="owner.name", read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "userId",
            "ownerName",
            "guestCount",
            "bathroomCount",
            "roomCount",
            "title",
            "description",
            "price",
            "locationValue",
            "category",
            "imageSrc",
            "createdAt",
        ]

    # patch method
    def update(self, instance, validated_data):
        if "imageSrc" in validated_data:
            instance.image_src = validated_data.pop("imageSrc", None)
        if "userId" in validated_data:
            instance.owner = validated_data.pop("userId", None)
        instance.save()
        return instance
