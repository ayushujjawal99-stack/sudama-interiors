# core/context_processors.py
# Runs once per request.
# Makes footer data available on ALL templates globally.

from services.models import Service
from products.models import ProductCategory


def footer_data(request):
    return {
        'footer_services': (
            Service.objects
            .select_related('category')
            .order_by('category__name', 'name')[:6]
        ),
        'footer_product_categories': (
            ProductCategory.objects
            .order_by('name')
        ),
    }