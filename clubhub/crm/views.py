from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from . forms import *
from .tables import *
from django_tables2 import SingleTableView
from django.core.exceptions import ObjectDoesNotExist
import datetime

from .models import *

home_url ="crm:index"
dash_url = "crm:dashboard"
back_btn = 'back_btn'
show_sidebar = 'show_sidebar'

#HOME Page
class HomePageView(generic.TemplateView):
    template_name = "crm/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = False
        return context

#REGISTER pages
class RegisterFormView(generic.FormView):
    template_name = "crm/register.html"
    form_class= RegisterForm
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = False
        context[back_btn] = home_url
        return context
    
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        object = User.objects.get(username=username)
        if object.approved:
            self.request.session['user_id'] = object.id
            self.success_url =  reverse('crm:dashboard')
        else:
            self.success_url =  reverse('crm:pending')
        return super(RegisterFormView, self).form_valid(form)

class PendingRegisterView(generic.TemplateView):
    template_name = 'crm/pending.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['application_type'] = "account"
        context[back_btn] = home_url
        return context

#LOGIN/OUT Pages
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
        context[back_btn] = home_url
        return context

def user_logout(request):
    request.session['user_id'] = None
    return redirect('crm:index')

#DASHBOARD Views
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
            context['club_table'] = ClubTable(Club.objects.all())
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
    model = User
    #fields = None
    def get(self, request, approved,pk) -> HttpResponse:
        self.user = User.objects.get(id=pk)
        approved_value = approved.lower() == 'true'
        if approved_value:
            self.user.approved = True
            self.user.save()
        else:
            #delete user if not approved
            self.user.delete()
            print('false')
            return redirect('crm:dashboard')
        return super().get(request)
    def get_success_url(self):
        return reverse('crm:dashboard')
#TODO approve club user 

#USER views
#TODO user profile (detailView) 
#TODO user update profile (updateView)

#CLUB views
class ClubCreateView(generic.CreateView):
    model = Club
    template_name = 'crm/create_club.html'
    form_class = ClubForm
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = True
        context[back_btn] = dash_url
        return context
    def form_valid(self, form):
        #club = form.save()
        form.clean()
        return super().form_valid(form)
    def get_success_url(self) :
        
        return reverse('crm:dashboard')    

#TODO club list (listView)

#TODO add club validity
#TODO list events
class ClubDetailView(generic.DetailView):
    model = Club
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        club = self.get_object()
        date = club.club_created.date()
        u_id= self.request.session.get('user_id')
        u = User.objects.get(id=u_id)
        context[show_sidebar] = True
        context[back_btn] = dash_url
        context['created'] = date.strftime("%B %Y")
        context['u'] = u
        return context


#EVENT views 
#TODO event create(createView)
#TODO event list (listView)
#TODO event join 
#TODO event approval (trigger for event approval)
    
#REPORTS
#only accessible by admin
# displays view results
