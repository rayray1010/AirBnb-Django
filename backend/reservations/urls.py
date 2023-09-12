from django.contrib import admin
from django.urls import path, include
from .views import (RetriveReservationView, ReservationCreateView)


urlpatterns = [
    # Google 登入的回調 URL，用於處理實際登入過程
    path('<int:user_id>/', RetriveReservationView.as_view()),
    path('', ReservationCreateView.as_view()),
]
