from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.RegisterView.as_view(), name='register'),
  path('add_key/', views.add_key, name='add_key'),
  path('login_with_yubikey/', views.login_with_yubikey, name='login_with_yubikey'),
]