from django.http import HttpResponseRedirect
from django.urls import reverse

class CheckLoggedIn:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == reverse('crm:dashboard'):
        #if user not logged in 
            if not request.session.get('user_id'):
                return HttpResponseRedirect(reverse('crm:index'))
        return response
