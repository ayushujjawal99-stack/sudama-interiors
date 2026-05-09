from django.shortcuts import get_object_or_404, render

from .models import Service


def services_home(request):
    return render(
        request,
        "services.html",
        {"services": Service.objects.order_by("title")},
    )


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(
        request,
        "service_detail.html",
        {
            "service": service,
            "related_services": Service.objects.exclude(pk=service.pk).order_by("title")[:3],
            "meta_title": f"{service.title} | Sudama Interiors",
            "meta_description": service.short_description,
        },
    )
