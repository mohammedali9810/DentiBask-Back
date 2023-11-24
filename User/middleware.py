# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
class RedirectIfAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is authenticated and trying to access login or register pages
        if request.user.is_authenticated and request.path in [reverse('login'), reverse('register')]:
            return JsonResponse({"redirect": reverse('index')})  # Signal a redirect to the frontend

        return response
