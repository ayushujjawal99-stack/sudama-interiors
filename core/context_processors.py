from services.models import Service


def site_navigation(request):
    return {
        "nav_services": Service.objects.order_by("id"),
        "brand_phone": "+91 98765 43210",
        "brand_email": "studio@sudamainteriors.com",
        "brand_location": "Premium interior services in Darbhanga, Bihar",
    }
