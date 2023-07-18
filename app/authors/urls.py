from authors.views import SignUpAuthorView
from django.contrib.auth.views import LogoutView
from django.urls import re_path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    re_path(r"^authors/signup/$",
            SignUpAuthorView.as_view(), name="author-signup"),
    re_path(r"^authors/login/$",
            obtain_auth_token, name="author-login"),
    re_path(r"^authors/logout/$",
            LogoutView.as_view(), name="author-logout"),
]
