from django.http import HttpResponse
from django.template import loader

from .models import App, Version, Rating
from .utils import first, ChartData, ChartDataset, ChartMarker


def index(request):
    """
    main page

    :param request: request
    :return: response
    """
    app_list = App.objects.all
    template = loader.get_template('timeline/dashboard.html')
    context = {
        'app_list': app_list,
        'title': 'Dashboard'
    }
    return HttpResponse(template.render(context, request))


def releases(request):
    """
    releases page

    :param request: request
    :return: response
    """
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
    """
    ratings page

    :param request: request
    :return: response
    """
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

    for version in Version.objects.all():
        timeline_item = first(chart_data.timeline, condition=lambda x: x >= version.pub_date)
        timeline_index = chart_data.timeline.index(timeline_item)

        marker_text = '%s#%s' % (version.app.name_without_os(), version.name)
        chart_data.markers.append(ChartMarker(version.app.name, timeline_index, marker_text))

    context = {
        'app_list': app_list,
        'title': 'Ratings',
        'chart_data': chart_data
    }
    return HttpResponse(template.render(context, request))
