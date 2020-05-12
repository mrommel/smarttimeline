from django.core import serializers
from django.http import JsonResponse

from cms.models import Content


def content(request, content_id):
    """
    content

    :param content_id:
    :param request: request
    :return: response
    """
    try:
        content_data = Content.objects.get(pk=content_id)
    except Content.DoesNotExist:
        content_data = None

    paragraph_response = []

    for paragraph in content_data.paragraphs():
        paragraph_item = {
            'headline': paragraph.headline,
            'text': paragraph.text
        }
        paragraph_response.append(paragraph_item)

    response_data = {
        'title': content_data.title,
        'paragraphs': paragraph_response
    }

    return JsonResponse(response_data)