from django import forms
from .models import MyUser 
from django.contrib.auth import authenticate
class LoginForm(forms.Form):
    username = forms.CharField(max_length = 25);
    password = forms.CharField(widget = forms.PasswordInput)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username = username).count() != 1:
            raise forms.ValidationError('Invalid Username')
        return username

    def clean(self):
        username = self.cleaned_data.get('username', '')
        passwd = self.cleaned_data.get('password', '')
        if username and passwd and not authenticate(username=username, password = passwd):
            raise forms.ValidationError('Username/Password doesnot match')
        return self.cleaned_data;


        


