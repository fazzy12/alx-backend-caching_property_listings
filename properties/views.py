from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property

@cache_page(60 * 15)
def property_list(request):
    """
    Renders a list of all properties, with the entire view response cached for 15 minutes.
    """
    properties = Property.objects.all()
    
    context = {
        'properties': properties
    }
    
    return render(request, 'properties/property_list.html', context)