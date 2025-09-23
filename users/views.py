from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request) :
    # work with databse
    # Transform Data
    # Data psss
    # http response / JSON response return 
    return HttpResponse("Well come to the task management System")

def contact(request) :
    return HttpResponse("<h1>This is Contact Page<h1/>")