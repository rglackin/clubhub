from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User


class CheckLoggedIn:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == reverse('crm:dashboard'):
        #if user not logged in or not approved
            user_id = request.session.get('user_id')
            approved = False
            try:
                user = User.objects.get(id = user_id)
                approved = user.approved
            except User.DoesNotExist:
                pass
            if not user_id or not approved :
                return HttpResponseRedirect(reverse('crm:index'))
        return response
