from django.urls import path, include

from .views import (ListingListCreaetView,
                    AddToFavoriteView, RetriveUpdateDeleteView, ListingReservationView, ListingOwnerView)

urlpatterns = [
    # Google 登入的回調 URL，用於處理實際登入過程
    path('reservation/<int:listing_id>/', ListingReservationView.as_view()),
    path('owner/', ListingOwnerView.as_view()),
    path('<int:pk>/favorite/', AddToFavoriteView.as_view()),
    path('<int:pk>/', RetriveUpdateDeleteView.as_view()),
    path('', ListingListCreaetView.as_view()),
]
