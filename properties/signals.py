from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

CACHE_KEY = 'all_properties'

@receiver([post_save, post_delete], sender=Property)
def invalidate_property_cache(sender, instance, **kwargs):
    """
    Signal receiver that invalidates the 'all_properties' cache key
    whenever a Property object is created, updated, or deleted.
    """
    cache.delete(CACHE_KEY)
    print(f"Cache key '{CACHE_KEY}' invalidated due to change in Property model.")