from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.RegisterView.as_view(), name='register'),
  path('add_key/', views.add_key, name='add_key'),
  path('delete_key/', views.delete_key, name='delete_key'),
  path('login_with_yubikey/',
  views.authenticate_with_yubikey, name='authenticate_with_yubikey'),
]