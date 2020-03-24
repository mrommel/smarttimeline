from django.http import HttpResponse
from django.template import loader

from .models import App

def index(request):
    app_list = App.objects.all
    template = loader.get_template('timeline/index.html')
    context = {
        'app_list': app_list,
    }
    return HttpResponse(template.render(context, request))