
from django.contrib import admin
from django.urls import path, include
from allauth.socialaccount.providers.google import views as google_views
from .views import (GoogleLoginView,  UserRedirectView,
                    UserRetriveMixin, UserRetriveMxin2, RegisterView, CustomLoginView)
from dj_rest_auth.views import LoginView

urlpatterns = [
    path('google/', google_views.oauth2_login, name='google_login'),
    # Google 登入的回調 URL，用於處理實際登入過程
    path("social-login/",
         GoogleLoginView.as_view(), name="google_login"),
    path('~redirect/', view=UserRedirectView.as_view(), name='redirect'),
    path('detail/', view=UserRetriveMixin.as_view()),
    path('<int:pk>', UserRetriveMxin2.as_view()),
    path('login/', CustomLoginView.as_view()),
    path('register/', RegisterView.as_view(), name='rest_register'),

]
