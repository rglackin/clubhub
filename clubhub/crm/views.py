from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from . forms import *
from .tables import *
from django_tables2 import SingleTableView
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.auth.decorators import login_required

# Authentication models and functions
from .models import User, ClubUser
#from django.contrib.auth.models import auth

#TODO make columns unique
show_sidebar = 'show_sidebar'
#this is the user that is logged in

class HomePageView(generic.TemplateView):
    template_name = "crm/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = False
        return context

class DashBoardView(SingleTableView):
    template_name = "crm/dashboard.html"
    model = User
    table_class = UserTable
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = True
        user = User.objects.get(id=self.request.session.get('user_id'))
        context['user'] = user
        coord = self.check_coord(user)
        context['coord'] = coord
        
        if user.is_admin:
            user_list = User.objects.filter(is_admin = False)
            context['user_list'] = user_list
            #context['user_table'] = UserTable(user_list)
        if coord:
            club_users = ClubUser.objects.filter(club = coord.club)
            context['club_users'] =  club_users
            context['club_users_table'] = ClubUserTable(club_users)
        return context

    def check_coord(self, session_user):
        try:
            return ClubUser.objects.get(user=session_user.id, is_coord = True)
        except ObjectDoesNotExist as e:
            print(e)
            return None


class ApproveUserView(generic.RedirectView):
    
    print("e")

def user_logout(request):
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
            self.success_url = reverse('crm:dashboard')
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context[show_sidebar] = False
        return context
class LogoutView():
    template_name = 'crm/logout.html'
    

