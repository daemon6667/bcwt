from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateView
from resources.models import EnabledResources


def view_MainPage(request):
    return HttpResponse("%s" % EnabledResources)

