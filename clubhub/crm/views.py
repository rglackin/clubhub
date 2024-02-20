from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from . forms import *
from django.contrib.auth.decorators import login_required

# Authentication models and functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout




class HomePageView(generic.TemplateView):
    template_name = "crm/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context



class RegisterFormView(generic.FormView):
    template_name = "crm/register.html"
    form_class= RegisterForm
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context
    
    def form_valid(self, form):
        object =form.save()
        self.success_url =  reverse('crm:index')
        return super(RegisterFormView, self).form_valid(form)

"""def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        
        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("my-login")
        


    context = {'registerform':form}

    return render(request, 'crm/register.html', context=context )

"""



def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                
                auth.login(request, user)

                return redirect("dashboard")

    context = {'loginform':form}

    return render(request, 'crm/my-login.html', context=context )


def user_logout(request):

    auth.logout(request)

    return redirect("")




@login_required(login_url="my-login")
def dashboard(request):

    return render(request, 'crm/dashboard.html' )

# superuser oisinfrizzell password Curry123






