# import json

# from django import forms

# from u2flib_server import u2f

# class KeyRegistrationForm(forms.Form):
#     response = forms.CharField()

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user')
#         self.request = kwargs.pop('request')
#         self.appId = kwargs.pop('appId')
#         return super(SecondFactorForm, self).__init__(*args, **kwargs)