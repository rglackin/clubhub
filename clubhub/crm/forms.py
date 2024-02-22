
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
        cleaned_data = super(RegisterForm, self).clean()
        user = User(**cleaned_data)  
        user.clean_username()  
        user.clean_password()  
        user.clean_email()  
        user.clean_phone_no()  

# Authenticate a user
        
class LoginForm(forms.Form):

    username = forms.CharField(widget=TextInput())     
    password = forms.CharField(widget=PasswordInput())      
    def authenticate(self, name, passwd):
        try:
            record = User.objects.get(username = name, password = passwd)
        except:
            record = None
        return record
    def clean(self):
        
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = self.authenticate(username, password)
        if not user:
            raise forms.ValidationError("Sorry, that login was Invalid. Please try again.")
        return self.cleaned_data
    def login(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = self.authenticate(username, password)
        return user





