from django.views.decorators.cache import cache_page
from django.http import JsonResponse
# from .models import Property # No longer needed if only using utils
from .utils import get_all_properties # <-- NEW IMPORT

@cache_page(60 * 15)
def property_list(request):
    """
    Retrieves all properties using the low-level cache utility and returns them as JSON.
    """
    properties = get_all_properties()
    
    data = list(properties)
    
    return JsonResponse({'data': data}, safe=False)
