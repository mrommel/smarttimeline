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

    plan_list = Plan.objects.all

    template = loader.get_template('roadmap/dashboard.html')
    context = {
        'title': 'Dashboard',
        'plan_list': plan_list
    }
    return HttpResponse(template.render(context, request))


def roadmap(request, roadmap_id):
    """
    roadmap page

    :param roadmap_id: id of roadmap
    :param request: request
    :return: response
    """

    try:
        plan = Plan.objects.get(pk=roadmap_id)
    except Plan.DoesNotExist:
        plan = None

    template = loader.get_template('roadmap/roadmap.html')
    context = {
        'title': plan.name,
        'plan': plan
    }
    return HttpResponse(template.render(context, request))