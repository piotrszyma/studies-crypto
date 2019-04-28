import json

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView
from django.shortcuts import render
from django.shortcuts import redirect

from u2flib_server import u2f
from . import models


class RegisterView(generic.CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'registration/register.html'


def get_origin(request):
    return '{scheme}://{host}'.format(
        scheme=request.scheme,
        host=request.get_host(),
    )

def add_key(request):
  if request.method == 'GET':
    origin = get_origin(request)
    u2f_request = u2f.begin_registration(origin, [])
    request.session['u2f_request'] = u2f_request
    return render(request, 'fido/add_key.html', {'u2f_request': json.dumps(request.session['u2f_request'])})
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
  return redirect('home')
