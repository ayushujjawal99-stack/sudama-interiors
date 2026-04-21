from services.models import Service
from products.models import ProductCategory
from .site_content import fallback_product_cards, fallback_service_cards, product_groups_from_queryset, service_card_from_model


def footer_data(request):
    services = [
        service_card_from_model(service)
        for service in (
            Service.objects
            .select_related("category")
            .order_by("category__name", "name")[:6]
        )
    ]
    product_categories = product_groups_from_queryset(
        ProductCategory.objects.prefetch_related("products").order_by("name")
    )

    if not services:
        services = [
            service
            for group in fallback_service_cards()
            for service in group["services"]
        ][:6]

    if not product_categories:
        product_categories = fallback_product_cards()

    return {
        "footer_services": services,
        "footer_product_categories": product_categories,
    }
