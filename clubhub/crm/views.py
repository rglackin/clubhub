from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from . forms import *
#from django.contrib.auth.decorators import login_required

# Authentication models and functions
#from .models import User
from django.contrib.auth.models import auth

#TODO make columns unique
show_sidebar = 'show_sidebar'
#this is the user that is logged in

class HomePageView(generic.TemplateView):
    template_name = "crm/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = False
        return context

class DashBoardView(generic.TemplateView):
    template_name = "crm/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = True
        #context['user'] = session_user
        return context

def user_logout(request):
    #auth.logout(request)
    request.session['user_id'] = None
    return redirect('crm:index')

class RegisterFormView(generic.FormView):
    template_name = "crm/register.html"
    form_class= RegisterForm
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = False
        return context
    
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        object = User.objects.get(username=username)
        if object.approved:
            self.request.session['user_id'] = object.id
            self.success_url =  reverse('crm:index')
        else:
            self.success_url =  reverse('crm:pending')
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
class PendingRegisterView(generic.TemplateView):
    template_name = 'crm/pending.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['application_type'] = "account"
        return context


class LoginView(generic.FormView):
    template_name = 'crm/login.html'
    form_class = LoginForm
    def form_valid(self, form):
        object = form.login() 
        self.request.session['user_id'] = object.id
        if object.approved == False:   
            self.success_url = reverse('crm:pending')
            
        else:
            self.success_url = reverse('crm:index')
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context[show_sidebar] = False
        return context
class LogoutView():
    template_name = 'crm/logout.html'
    
"""def my_login(request):

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

    return render(request, 'crm/my-login.html', context=context )"""


#def user_logout(request):

 #   auth.logout(request)

  #  return redirect("")"""
