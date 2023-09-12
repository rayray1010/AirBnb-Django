from django.db import models

# Create your models here.
"""
 id String @id @default(auto()) @map("_id") @db.ObjectId
  title String
  description String
  imageSrc String
  createdAt DateTime @default(now())
  category  String
  roomCount Int
  bathroomCount Int
  guestCount Int
  locationValue String
  userId String @db.ObjectId
  price Int

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)
  reservations Reservation[]
"""


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image_src = models.CharField(blank=True, null=True, max_length=100)
    category = models.CharField(blank=True, null=True, max_length=100)
    room_count = models.IntegerField(default=0)
    bathroom_count = models.IntegerField(default=0)
    guest_count = models.IntegerField(default=0)
    location_value = models.CharField(max_length=100,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
