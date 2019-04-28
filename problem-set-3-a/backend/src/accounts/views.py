import json

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone

from u2flib_server import u2f
from . import models
from . import forms



class RegisterView(generic.CreateView):
  form_class = forms.RegisterForm
  success_url = reverse_lazy('login')
  template_name = 'registration/register.html'


def get_origin(request):
    return '{scheme}://{host}'.format(
        scheme=request.scheme,
        host=request.get_host(),
    )


def delete_key(request):
  models.U2FKey.objects.filter(user=request.user).delete()
  messages.info(request, 'Yubikey deleted')
  return redirect('home')


def add_key(request):
  if request.method == 'GET':
    origin = get_origin(request)
    u2f_request = u2f.begin_registration(origin, [])
    request.session['u2f_request'] = u2f_request
    context = {'u2f_request': json.dumps(request.session['u2f_request'])}
    return render(request, 'registration/add_key.html', context)
  u2f_response = request.POST['response']
  origin = get_origin(request)
  device, attestation_cert = u2f.complete_registration(
    request.session['u2f_request'], u2f_response)
  models.U2FKey.objects.update_or_create(
    user=request.user,
    defaults={
      'public_key': device['publicKey'],
      'key_handle': device['keyHandle'],
      'app_id': device['appId'],
      },
  )
  messages.success(request, 'Yubikey configured.')
  del request.session['u2f_request']
  # For first usage, assume authenticated.
  request.session['yubikey_authenticated'] = True
  return redirect('home')

def authenticate_with_yubikey(request):
  u2f_key = models.U2FKey.objects.filter(user=request.user).first()

  if not u2f_key:
    messages.error(request, 'Cannot authenticate with yubikey. '
                            'You need to set it first.')
    return redirect('home')

  if request.method == 'GET':
    origin = get_origin(request)
    u2f_request = u2f.begin_authentication(u2f_key.app_id, [{
      'publicKey': u2f_key.public_key,
      'keyHandle': u2f_key.key_handle,
      'appId': u2f_key.app_id,
      'version': 'U2F_V2'}])
    request.session['u2f_request'] = u2f_request
    context = { 'u2f_request': json.dumps(u2f_request) }
    return render(request, 'registration/login_with_key.html', context)
  u2f_response = request.POST['response']
  device, login_counter, _ = u2f.complete_authentication(
    request.session['u2f_request'], u2f_response)
  u2f_key.last_used_at = timezone.now()
  u2f_key.save()
  messages.success(request, 'authenticated with yubikey')
  request.session['yubikey_authenticated'] = True
  del request.session['u2f_request']
  return redirect('home')
