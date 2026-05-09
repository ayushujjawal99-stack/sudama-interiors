from django.shortcuts import get_object_or_404, render

from .catalog import catalog_for
from .models import Service


def services_home(request):
    return render(
        request,
        "services.html",
        {
            "services": Service.objects.order_by("id"),
            "meta_title": "Interior Services in Darbhanga & Bihar | Sudama Interiors",
            "meta_description": "Explore premium interior services in Darbhanga and Bihar: uPVC windows, false ceiling, ACP cladding, panels, laminates, UV marble sheets, and SS railing.",
        },
    )


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    catalog = catalog_for(service.slug)
    return render(
        request,
        "service_detail.html",
        {
            "service": service,
            "catalog": catalog,
            "related_services": Service.objects.exclude(pk=service.pk).order_by("id")[:3],
            "meta_title": f"{service.title} in Darbhanga & Bihar | Sudama Interiors",
            "meta_description": service.short_description,
        },
    )
