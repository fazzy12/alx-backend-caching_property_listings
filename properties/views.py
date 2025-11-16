from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

@cache_page(60 * 15)
def property_list(request):
    """
    Retrieves all properties and returns them as JSON, with the response cached in Redis.
    """
    properties = Property.objects.all().values('title', 'description', 'price', 'location')
    
    data = list(properties)
    
    return JsonResponse({'data': data}, safe=False)