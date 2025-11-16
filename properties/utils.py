from django.core.cache import cache
from .models import Property

CACHE_KEY = 'all_properties'
CACHE_TIMEOUT = 3600

def get_all_properties():
    """
    Checks the low-level cache for the list of properties. 
    If not found, fetches them from the database and stores them in cache for 1 hour.
    """
    properties = cache.get(CACHE_KEY)
    
    if properties is not None:
        return properties
    
    
    properties = Property.objects.all().values('title', 'description', 'price', 'location')
    
    cache.set(CACHE_KEY, properties, CACHE_TIMEOUT)
    
    return properties