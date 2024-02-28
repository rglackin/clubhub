from typing import Dict
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from . forms import *
from .tables import *
from django_tables2 import SingleTableView
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.views import View
from django.views.generic import DetailView
from .models import Club
#from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.db.models import Q


from .models import *

home_url ="crm:index"
dash_url = "crm:dashboard"
back_btn = 'back_btn'
show_sidebar = 'show_sidebar'

def get_session_user(request):
    user_id = request.session['user_id']
    return User.objects.get(id=user_id)
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

"""class LogoutView():
    template_name = 'crm/logout.html'
"""
"""
class ClubDetailView(DetailView):
    model = Club
    template_name = 'crm/club_detail.html'  # Adjust this path as needed
    context_object_name = 'club'


    # when redircting rory jsut add if statment
    
   # if club_id:
            # Replace the URLs with the ones you want to redirect to based on club_id
          #  if club_id == '1':
              #  return redirect(reverse('crm:club_detail', kwargs={'pk': club_id}))
           # elif club_id == '2':
               # return redirect('url')
"""
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
            #context['coord_club'] = coord.club.club_id
            context['club_users'] =  club_users
            context['club_users_table'] = ClubUserTable(club_users)
        if not user.is_admin:
            memberships = ClubUser.objects.filter(user = user)
            context['memberships'] = memberships
            context['member_table'] = MembershipTable(memberships) 
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
    def get_redirect_url(self):
        return reverse('crm:dashboard')
#TODO approve club user 

#USER views
#TODO user profile (detailView)
class UserDetailView(generic.DetailView):
    model = User
    template_name = "crm/user_profile.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = True
        context['user'] = User.objects.get(id= self.kwargs['pk'])
        return context
#TODO user update profile (updateView)
class UserUpdateView(generic.UpdateView):
    model = User
    fields = ["phone_no","email"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = True
        context['user'] = User.objects.get(id= self.kwargs['pk'])
        return context
    def get_success_url(self) -> str:
        return reverse('crm:dashboard'  )
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
    def get_redirect_url(self):
        return reverse('crm:dashboard')    

#TODO club list (listView)
class ClubListView(generic.ListView):
    template_name = 'crm/clubs_list.html'
    model = Club 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = True
        return context
    """def get(self, request, *args, **kwargs):
        clubs = Club.objects.all()
        return render(request, self.template_name, {'clubs': clubs})"""
    
class ApproveClubUserView(generic.RedirectView):
    model = ClubUser
    #fields = None
    def get(self, request, approved,pk) -> HttpResponse:
        self.clubUser = ClubUser.objects.get(id=pk)
        approved_value = approved.lower() == 'true'
        if approved_value:
            self.clubUser.is_approved = True
            self.clubUser.save()
        else:
            #delete user if not approved
            self.clubUser.delete()
            print('false')
            return redirect('crm:dashboard')
        return super().get(request)
    def get_redirect_url(self):
        return reverse('crm:dashboard')



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
        context['is_member'] = self.is_member(u)
        return context
    def is_member(self,user):
        club = self.get_object()
        try:
            member = ClubUser.objects.get(user = user,club = club )
        except ObjectDoesNotExist:
            return False
        return True
def joinClub(request, pk):
    club_id = pk 
    user_id = request.session['user_id']
    #user = User.objects.get(id=user_id)
    membership = ClubUser.create(club_id,user_id)
    membership.save()
    return redirect('crm:dashboard')
#BUG redirect view not working idk y
#TODO user can join max of 3 clubs
class ClubJoinView(generic.RedirectView):
    model = ClubUser
    #fields = None
    def get(self, request, pk):
        #self.user = User.objects.get(id=pk)
        logging.debug('GET called')
        club_id =  self.kwargs['pk'] 
        user_id = self.request.session['user_id']
        #user = User.objects.get(id=user_id)
        membership = ClubUser.create(club_id,user_id)
        membership.save()
        return super().get(request)
    
    def get_redirect_url(self):
        logging.debug('redirect called')
        return redirect('crm:dashboard')
    

class ClubCoordinatorCreateView(generic.FormView):
    model = ClubUser
    template_name = 'crm/clubuser_form.html'
    form_class = ClubCoordForm
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = True
        #context[back_btn] = dash_url
        return context
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        users = User.objects.filter(is_admin = False)
        #ids = users.values_list('id', flat=True)
        kwargs['user_queryset'] = users

        return kwargs
    def form_valid(self, form: Any):
        object = form.save(commit = False)
        object.is_coord = True
        club_id = self.kwargs['pk']
        object.club = Club.objects.get(club_id= club_id)
        object.is_approved = True
        object.save()
        self.success_url = reverse('crm:club_detail', kwargs={'pk':club_id})
        return super().form_valid(form)
    
#EVENT views 

class EventCreateView(generic.CreateView):
    model = Events
    form_class = EventForm
    def get_context_data(self, **kwargs) :
        context =super().get_context_data(**kwargs)
        context[show_sidebar] = True
        return context
    def form_valid(self, form):
        object = form.save(commit=False)
        club_id = self.kwargs['pk']
        object.club = Club.objects.get(club_id=club_id)
        object.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('crm:dashboard')

class EventListView(generic.ListView):
    model = Events
    club = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = True
        context['club'] = self.club
        return context
    def get_queryset(self):
        club_id = self.kwargs['pk']
        self.club = Club.objects.get(club_id =club_id)
        now = timezone.now()
        querySet =  Events.objects.filter(date__gte = now, club =self.club )
        
        return querySet
#Event detail
class EventDetailView(generic.DetailView):
    model = Events
    def get_context_data(self, **kwargs):
        user = get_session_user(self.request)
        event = self.get_object()
        
        context = super().get_context_data(**kwargs)
        context[show_sidebar] = True
        club_user = ClubUser.objects.get(user = user, club = event.club)
        if club_user.is_coord:
            context['coord'] = True
        try:
            registered= EventUser.objects.get(user=user,event=event)
            approved= False
            if registered.is_approved:
                approved = True
            context['registered'] = registered
            context['approved'] = approved
        except ObjectDoesNotExist:
            pass
        return context
    """def is_member(self,user):
        #club = self.get_object()
        try:
            return ClubUser.objects.get(user = user,club = club )
        except ObjectDoesNotExist:
            return False"""

def event_join(request, pk):
    user = get_session_user(request)
    event = Events.objects.get(event_id=pk)

    object = EventUser.create(user,event)
    object.save()
    return redirect('crm:dashboard')


class EventManageView(SingleTableView):
    model = EventUser
    context_object_name = "user_list"
    template_name = 'crm/events_manage.html'
    table_class = EventManageTable
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['event'] = Events.objects.get(event_id = self.kwargs['pk'])
        context[show_sidebar] = True
        return context
    def get_queryset(self):
        event_id = self.kwargs['pk']
        object_list = EventUser.objects.filter(
            event_id=event_id)
        return object_list

def event_approve(request, pk,approved):
    event_user = EventUser.objects.get(id=pk)
    event_id = event_user.event.event_id
    if approved.lower() == 'true':
        event_user.is_approved = True
        event_user.save()
    else:
        event_user.delete()
    return redirect('crm:event_manage', event_id)
#REPORTS
#only accessible by admin
# displays view results
