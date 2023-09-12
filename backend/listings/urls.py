from django.urls import path, include

from .views import (ListingListCreaetView,
                    AddToFavoriteView, RetriveUpdateView)

urlpatterns = [
    # Google 登入的回調 URL，用於處理實際登入過程
    path('<int:pk>/favorite/', AddToFavoriteView.as_view(), name='add_to_favorite'),
    path('<int:pk>/', RetriveUpdateView.as_view()),
    path('', ListingListCreaetView.as_view()),
]
