from datetime import datetime
from rest_framework import serializers
from dj_rest_auth.serializers import JWTSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from listings.serializer import ListingSerializer
from reservations.serializer import ReservationSerializer
# from dj_rest_auth.registration.serializers import LoginSerializer
from .models import CustomUser

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    favorites = serializers.SerializerMethodField()

    def get_favorites(self, obj):
        # 使用 ListingSerializer 將收藏清單序列化
        favorites = obj.favorites.all()
        serializer = ListingSerializer(favorites, many=True)
        return serializer.data

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'name',
            'image',
            'created_at',
            'updated_at',
            'favorites',
        ]


class UserRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)


class SocialLoginSerializer(JWTSerializer):
    def get_user(self, obj):
        user = self.user
        print(user)
        return user


# class LoginSerializer(LoginSerializer):
#     username = None


class RegisterSerializer(serializers.ModelSerializer):
    id: serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('name', 'password', 'email', 'id')

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
