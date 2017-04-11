import pprint

from django.http import JsonResponse

from .models import Story

def stories(request, count=10):

    count = int(count)

    query_set = Story.objects.order_by('?')[:count].values()

    response_dict = {
        'count': count,
        'data': list(query_set),
    }

    return JsonResponse(response_dict)
