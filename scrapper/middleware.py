from django.shortcuts import redirect
from django.urls import reverse

class RedirectIfNotLoggedInMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('login')
        signin_url = reverse('signin')
        logout_url = reverse('logout')
        
        if not request.user.is_authenticated and request.path not in [login_url, signin_url, logout_url]:
            return redirect('login')
        
        response = self.get_response(request)
        return response
