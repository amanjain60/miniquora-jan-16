from django import forms
from .models import MyUser 
from django.contrib.auth import authenticate
class LoginForm(forms.Form):
    username = forms.CharField(max_length = 25);
    password = forms.CharField(widget = forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.authenticated_user = None;
        super(LoginForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        data_username = self.cleaned_data['username']
        if MyUser.objects.filter(username = data_username).count() != 1:
            raise forms.ValidationError('Invalid Username')
        return data_username

    def clean(self):
        data_username = self.cleaned_data.get('username', '')
        data_passwd = self.cleaned_data.get('password', '')
        user = authenticate(username=data_username, password = data_passwd)
        if data_username and data_passwd and not user:
            raise forms.ValidationError('Username/Password doesnot match')
        self.authenticated_user = user
        return self.cleaned_data;

class ForgotPassword(forms.Form):
    username = forms.CharField(max_length = 100)

    def clean_username(self):
        data_username = self.cleaned_data.get('username', '')
        if data_username and not MyUser.objects.filter(username = data_username).exists():
            raise forms.ValidationError('Invalid Username')
        return data_username
