from django.urls import resolve
from django.shortcuts import redirect

from accounts import models

def yubikey_middleware(get_response):

    def middleware(request):
        if not request.user.is_authenticated:
          return get_response(request)

        if not models.U2FKey.objects.filter(user=request.user).exists():
          return get_response(request)

        yubikey_authenticated = request.session.get('yubikey_authenticated')

        if yubikey_authenticated:
          return get_response(request)

        is_yubikey_auth_path = (
          resolve(request.path_info).url_name == 'authenticate_with_yubikey')

        if not is_yubikey_auth_path:
          return redirect('authenticate_with_yubikey')

        response = get_response(request)

        return response

    return middleware