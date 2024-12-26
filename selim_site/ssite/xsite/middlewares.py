from django.shortcuts import redirect
from django.urls import reverse

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = [
            reverse('login'),
            reverse('register'),
        ]

        if not request.user.is_authenticated and request.path not in allowed_urls:
            return redirect('login') 
        response = self.get_response(request)
        return response
