from django.urls import path

from .views import registration, LoginView, UserLogout, profile, activate
urlpatterns = [
    path("register/", registration, name = 'register'),
    path("login/", LoginView.as_view(), name = 'login'),
    path('logOut/', UserLogout, name = 'logout'),
    path("profile/", profile, name = 'profile'),
    # path("activate/<uid64>/<token>/onerender.com/", activate, name = 'active'),
    path("activate/<uid64>/<token>", activate, name = 'active'),

    # path("profile/"),
]
