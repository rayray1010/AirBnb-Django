from django.contrib import admin
from django.urls import path, include
from .views import (RetriveReservationView,
                    ReservationCreateView, ListReservationFromUserView, ReservationByListingIdView, ReservationByListingOwnerView)


urlpatterns = [
    # Google 登入的回調 URL，用於處理實際登入過程
    path('user/', ListReservationFromUserView.as_view()),
    path('owner/', ReservationByListingOwnerView.as_view()),
    path('<int:pk>/', RetriveReservationView.as_view()),
    path('', ReservationCreateView.as_view()),
]
