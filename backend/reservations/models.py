from django.db import models
# Create your models here.


"""
id String @id @default(auto()) @map("_id") @db.ObjectId
userId String @db.ObjectId
listingId String @db.ObjectId  
startDate DateTime
endDate DateTime
totalPrice Int
createdAt DateTime @default(now())

user User @relation(fields: [userId], references: [id], onDelete: Cascade)
listing Listing @relation(fields: [listingId], references: [id], onDelete: Cascade)
"""


class Reservation(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    user_id = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    listing_id = models.ForeignKey(
        "listings.Listing", on_delete=models.CASCADE)
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
