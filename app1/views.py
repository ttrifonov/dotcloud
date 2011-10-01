from django.http import HttpResponse

from django.contrib.auth.models import User

def home(request):
    us = User.objects.all()
    return HttpResponse("App 1<a href='/secure/'>Secure</a>")

def secure(request):
    return HttpResponse("App 1 (secure) <a href='/'>Home</a>")

