
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crm.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

# Create a user
class RegisterForm(forms.ModelForm):
    

    class Meta:
        model = User
        fields = ('username','password','phone_no','email')
        


# Authenticate a user
        
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())     
    password = forms.CharField(widget=PasswordInput())      





