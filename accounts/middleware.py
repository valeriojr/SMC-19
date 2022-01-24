from django.http import HttpResponseRedirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        change_password_path = reverse('accounts:change-password')

        if request.path != change_password_path and request.user.is_authenticated and request.user.first_login:
            return HttpResponseRedirect(change_password_path)
        else:
            return self.get_response(request)