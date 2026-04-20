from django.shortcuts import get_object_or_404, render
from .models import Service, ServiceCategory
from .content import SERVICE_CONTENT


def services_home(request):
    categories = ServiceCategory.objects.prefetch_related("services").order_by("name")
    return render(request, "services/services_home.html", {
        "categories": categories,
    })


def service_detail(request, slug):
    service = get_object_or_404(
        Service.objects.select_related("category"),
        slug=slug,
    )

    related_services = (
        Service.objects.select_related("category")
        .filter(category=service.category)
        .exclude(pk=service.pk)[:4]
    )

    # ✅ SAFE CONTENT FETCH
    content = SERVICE_CONTENT.get(slug) or {}

    intro = content.get("intro", "")
    sections = content.get("sections", [])
    construction_layout = content.get("construction_layout", None)
    door_specs = content.get("door_specs", None)

    hero_description = (
        service.short_description
        or service.description
        or f"Premium {service.name.lower()} solutions with modern design and long-lasting quality."
    )

    meta_title = service.meta_title or f"{service.name} | Sudama Interiors"
    meta_description = (
        service.meta_description
        or service.short_description
        or service.description
    )

    return render(request, "services/service_detail.html", {
        "service": service,
        "hero_description": hero_description,
        "meta_title": meta_title,
        "meta_description": meta_description,

        # 🔥 FINAL DATA PIPELINE
        "intro": intro,
        "sections": sections,
        "construction_layout": construction_layout,
        "door_specs": door_specs,

        "service_highlights": [
            "Premium material quality",
            "Clean finishing standards",
            "Durable and long-lasting",
            "Modern design compatibility",
        ],

        "related_services": related_services,
    })