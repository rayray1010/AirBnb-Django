from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import RedirectView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import APIException
from .models import CustomUser
from .serializer import CustomLoginSerializer, UserRegisterSerializer, UserSerializer, SocialLoginSerializer, RegisterSerializer
from listings.serializer import CreateListingSerializer
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from drf_spectacular.utils import extend_schema


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'fuckyou detail'
    default_code = 'fuch you code'


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/"
    client_class = OAuth2Client


class GithubLoginView(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return "redirect-url"


class UserRetriveMixin(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        self.kwargs[self.lookup_field] = self.request.user.id
        return super().get(request, *args, **kwargs)


class UserRetriveMxin2(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    lookup_field = "pk"


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class CustomLoginView(LoginView):
    # allow any request
    permission_classes = [AllowAny]

    @extend_schema(
        request=CustomLoginSerializer,
        responses={200: UserSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserFavoritedListingView(generics.ListAPIView):
    serializer_class = CreateListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.favorites.all()
