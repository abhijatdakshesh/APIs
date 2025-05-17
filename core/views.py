from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the API! The server is running successfully.") 