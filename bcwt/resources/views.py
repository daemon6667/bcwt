from django.shortcuts import render
from django.http import HttpResponse
from resources.models import EnabledResources

# Create your views here.

def view_MainPage(request):
    return HttpResponse("%s" % EnabledResources)

