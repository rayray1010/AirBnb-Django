from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Create your models here.

"""
    id              String @id @default(auto()) @map("_id") @db.ObjectId
    name            String?
    email           String?   @unique
    emailVerified   DateTime?
    image           String?
    hashedPassword  String?
    createdAt       DateTime @default(now())
    updatedAt       DateTime @updatedAt
    favoriteIds     String[] @db.ObjectId

    accounts Account[]
    listings Listing[]
    reservations Reservation[]
"""


class CustomUser(AbstractUser):
    # 取消 default User 欄位
    username = None
    first_name = None
    last_name = None

    # custom field
    email = models.EmailField(_("email address"), unique=True)
    email_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorites = models.ManyToManyField(
        "listings.Listing", related_name="favorited_by")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
