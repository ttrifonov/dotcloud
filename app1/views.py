from django.http import HttpResponse
 
def home(request):
    return HttpResponse("App 1")

def secure(request):
    return HttpResponse("App 1 (secure) ")

