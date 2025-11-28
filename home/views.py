from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'home/home.html')

# Créez ces vues temporaires si elles n'existent pas
def events(request):
    return render(request, 'evenement/evenements.html')

def venues(request):
    return render(request, 'home/venues.html')

def organize(request):
    return render(request, 'home/organize.html')

def login(request):
    return render(request, 'home/login.html')