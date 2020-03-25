from django.http import HttpResponse
from django.template import loader
# import numpy as np

from .models import App, Version, Rating


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


class ChartDataset:

    def __init__(self, name, color, solid):
        self.name = name
        self.color = color
        self.solid = solid
        self.data = []


class ChartData:
    """A class that hold the chart data ready to be displayed"""

    def __init__(self):
        self.timeline = []
        self.datasets = []


def ratings(request):
    app_list = App.objects.all
    template = loader.get_template('timeline/ratings.html')

    chart_data = ChartData()

    for rating in Rating.objects.order_by('pub_date'):
        chart_data.timeline.append(rating.pub_date)

        dataset = next((x for x in chart_data.datasets if x.name == rating.app.name), None)
        if dataset is None:
            chart_dataset = ChartDataset(rating.app.name, rating.app.color, rating.app.solid)
            chart_dataset.data.append(rating.rating)
            chart_data.datasets.append(chart_dataset)
        else:
            dataset.data.append(rating.rating)

    # remove duplicates
    chart_data.timeline = list(set(chart_data.timeline))

    # sort
    chart_data.timeline.sort()

    context = {
        'app_list': app_list,
        'title': 'Ratings',
        'chart_data': chart_data
    }
    return HttpResponse(template.render(context, request))
