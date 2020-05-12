from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

# Create your views here.
from roadmap.models import Plan


def index(request):
    """
    main page

    :param request: request
    :return: response
    """

    try:
        plan = Plan.objects.get(pk=1)
    except Plan.DoesNotExist:
        plan = None

    template = loader.get_template('roadmap/dashboard.html')
    context = {
        'title': 'Dashboard',
        'plan': plan
    }
    return HttpResponse(template.render(context, request))
