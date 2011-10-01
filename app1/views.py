from django.http import HttpResponse
 
def home(request):
    return HttpResponse("App 1<a href='/secure/'>Secure</a>")

def secure(request):
    return HttpResponse("App 1 (secure) <a href='/'>Home</a>")

