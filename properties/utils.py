import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)

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


def get_redis_cache_metrics():
    """
    Connects to the Redis cache and retrieves keyspace hit/miss metrics to calculate the hit ratio.
    """
    try:
        redis_connection = get_redis_connection("default")
        info = redis_connection.info('Keyspace')
        
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)

        total_lookups = keyspace_hits + keyspace_misses
        
        hit_ratio = keyspace_hits / total_lookups if total_lookups > 0 else 0

        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_lookups': total_lookups,
            'hit_ratio': hit_ratio,
        }

        # Log the metrics
        logger.info(f"Redis Cache Metrics: Hits={keyspace_hits}, Misses={keyspace_misses}, Ratio={hit_ratio:.4f}")
        
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_lookups': 0,
            'hit_ratio': 0.0,
            'error': str(e)
        }
