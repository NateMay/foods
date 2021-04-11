
from review.models import UsdaWikiPairing, WikiCategory, WikiFood
from django import template
register = template.Library()

@register.inclusion_tag('review/stats.html')
def get_stats():
    return {
        'food_meta_count': WikiFood.objects.count(),
        'cat_meta_count': WikiCategory.objects.count(),
        'reviewed_foods': WikiFood.objects.filter(reviewed=True).count(),
        'complete': UsdaWikiPairing.objects.count(),
        'indexed': UsdaWikiPairing.objects.filter(indexed=True).count(),
    }
