
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crm.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

# Create a user
class RegisterForm(forms.ModelForm):
    

    class Meta:
        model = User
        fields = ('username','password','phone_no','email')

    def clean(self):
        cleaned_data = super().clean()
        user = User(**cleaned_data)  
        user.clean_username()  
        user.clean_password()  
        user.clean_email()  
        user.clean_phone_no()  


        


# Authenticate a user
        
class LoginForm(forms.Form):

    username = forms.CharField(widget=TextInput())     
    password = forms.CharField(widget=PasswordInput())      





