from django.urls import path, re_path, include
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('login/', login_view, name="login"),
    re_path(r'^accounts', login_view),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('password_reset/', PasswordResetView.as_view()),
    path('password_reset_done/', PasswordResetDoneView.as_view()),
    path('password_reset_confirm/', PasswordResetConfirmView.as_view()),
    path('password_reset_complete/', PasswordResetCompleteView.as_view()),
    path('', include('django.contrib.auth.urls'))
]
