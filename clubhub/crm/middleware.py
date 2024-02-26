from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User
import logging

class CheckLoggedIn:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path_list =[reverse('crm:dashboard'),reverse('crm:create_club')] 
        if request.path in path_list :
        #if user not logged in or not approved
            user_id = request.session.get('user_id')
            approved = False
            try:
                logging.debug('mw.call called')
                user = User.objects.get(id = user_id)
                approved = user.approved
            except User.DoesNotExist:
                logging.debug('mw.usernotexist called')
                pass
            if not user_id or not approved :
                logging.debug('mw.notuser called')
                return HttpResponseRedirect(reverse('crm:index'))
        return response

class CheckAdmin:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path_list =[reverse('crm:create_club')] 
        if request.path in path_list :
        #if user not logged in or not approved
            user_id = request.session.get('user_id')
            admin = False
            try:
                user = User.objects.get(id = user_id)
                admin = user.is_admin
            except User.DoesNotExist:
                pass
            if not user_id or not admin :
                return HttpResponseRedirect(reverse('crm:dashboard'))
        return response