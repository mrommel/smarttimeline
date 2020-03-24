from django.http import HttpResponse
from django.template import loader

from .models import App

"""
	Dashboard
"""
def index(request):
    app_list = App.objects.all
    template = loader.get_template('timeline/dashboard.html')
    context = {
        'app_list': app_list,
        'title': 'Dashboard'
    }
    return HttpResponse(template.render(context, request))


def releases(request):
    app_list = App.objects.all
    template = loader.get_template('timeline/releases.html')
    context = {
        'app_list': app_list,
        'title': 'Releases'
    }
    return HttpResponse(template.render(context, request))


def ratings(request):
    app_list = App.objects.all
    template = loader.get_template('timeline/ratings.html')
    context = {
        'app_list': app_list,
        'title': 'Ratings'
    }
    return HttpResponse(template.render(context, request))
