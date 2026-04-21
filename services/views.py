from django.http import Http404
from django.shortcuts import render

from core.site_content import (
    fallback_service_cards,
    find_fallback_service,
    service_card_from_model,
    service_groups_from_queryset,
)
from .content import SERVICE_CONTENT
from .models import Service, ServiceCategory


def services_home(request):
    groups = service_groups_from_queryset(
        ServiceCategory.objects.prefetch_related("services").order_by("name")
    )
    return render(
        request,
        "services/services_home.html",
        {"service_groups": groups or fallback_service_cards()},
    )


def _content_sections(content):
    sections = []
    for index, section in enumerate(content.get("sections", []), start=1):
        sections.append(
            {
                "title": section.get("title") or f"Service Detail {index}",
                "content": "",
                "items": section.get("items", []),
                "images": section.get("images", []),
                "order": index,
            }
        )
    return sections


def _model_sections(service, content):
    db_sections = [
        {
            "title": section.title,
            "content": section.content,
            "items": [],
            "images": [],
            "order": section.order,
        }
        for section in service.sections.all()
    ]
    return db_sections or _content_sections(content)


def _model_gallery(service):
    gallery = []
    for image in service.images.all()[:6]:
        try:
            url = image.image.url
        except ValueError:
            url = ""
        if url:
            gallery.append({"url": url, "alt": image.alt_text or service.name})
    return gallery


def _related_services(service):
    return [
        service_card_from_model(item)
        for item in (
            Service.objects.select_related("category")
            .filter(category=service.category)
            .exclude(pk=service.pk)[:4]
        )
    ]


def service_detail(request, slug):
    # Try to get service from DB, fallback to hardcoded content if not found
    service = Service.objects.select_related("category").filter(slug=slug).first()
    fallback_service = None
    
    if not service:
        fallback_service = find_fallback_service(slug)
        if not fallback_service:
            raise Http404("Service not found")

    content = SERVICE_CONTENT.get(slug) or {}

    if service:
        service_data = service_card_from_model(service)
        service_data["meta_title"] = service.meta_title
        service_data["meta_description"] = service.meta_description
        service_data["full_description"] = service.full_description
        sections = _model_sections(service, content)
        gallery_images = _model_gallery(service)
        related_services = _related_services(service)
    else:
        service_data = fallback_service
        sections = _content_sections(content)
        gallery_images = []
        related_services = [
            item
            for group in fallback_service_cards()
            for item in group["services"]
            if item["category_name"] == fallback_service["category_name"]
            and item["slug"] != fallback_service["slug"]
        ][:4]

    intro = (
        service_data.get("full_description")
        or content.get("intro")
        or service_data.get("short_description")
        or service_data.get("summary")
        or ""
    )
    hero_description = (
        service_data.get("short_description")
        or intro
        or f"Premium {service_data['name'].lower()} solutions with modern design and long-lasting quality."
    )
    meta_title = service_data.get("meta_title") or f"{service_data['name']} | Sudama Interiors"
    meta_description = (
        service_data.get("meta_description")
        or service_data.get("short_description")
        or intro
    )

    return render(
        request,
        "services/service_detail.html",
        {
            "service": service_data,
            "hero_description": hero_description,
            "meta_title": meta_title,
            "meta_description": meta_description,
            "intro": intro,
            "detail_sections": sections,
            "gallery_images": gallery_images,
            "construction_layout": content.get("construction_layout"),
            "door_specs": content.get("door_specs"),
            "service_highlights": [
                "Material choices matched to real site conditions",
                "Measured execution with clean finishing standards",
                "Durable detailing for long-term daily use",
                "Design compatibility across modern and classic spaces",
            ],
            "related_services": related_services,
        },
    )
