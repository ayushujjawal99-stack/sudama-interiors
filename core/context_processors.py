from services.models import Service


def site_navigation(request):
    return {
        "nav_services": Service.objects.order_by("title")[:6],
        "brand_phone": "+91 98765 43210",
        "brand_email": "studio@sudamainteriors.com",
        "brand_location": "Bespoke interiors across India",
    }
