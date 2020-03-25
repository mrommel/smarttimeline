from django.http import HttpResponse
from django.template import loader

from .models import App, Version


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
    release_list = Version.objects.order_by('-pub_date')

    last_month = 27
    for release_item in release_list:
        if release_item.pub_date.month != last_month:
            release_item.first = True
        else:
            release_item.first = False

        last_month = release_item.pub_date.month

    template = loader.get_template('timeline/releases.html')
    context = {
        'app_list': app_list,
        'title': 'Releases',
        'release_list': release_list
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
