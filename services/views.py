from django.http import Http404
from django.shortcuts import render

from core.site_content import (
    fallback_service_cards,
    find_fallback_service,
    service_groups_from_queryset,
)
from .content import SERVICE_CONTENT
from .models import ServiceCategory


def services_home(request):
    groups = service_groups_from_queryset(
        ServiceCategory.objects.prefetch_related("services").order_by("name")
    )
    return render(
        request,
        "services/services_home.html",
        {"service_groups": groups or fallback_service_cards()},
    )


# ============================= #
# SAFE SECTION BUILDER (FROM content.py)
# ============================= #

def _build_sections(content):
    sections = []
    for index, section in enumerate(content.get("sections", []), start=1):
        sections.append({
            "title": section.get("title") or f"Section {index}",
            "items": section.get("items", []),
            "images": section.get("images", []),
            "order": index,
        })
    return sections


# ============================= #
# MAIN VIEW
# ============================= #

def service_detail(request, slug):
    # PRIMARY: content.py
    content = SERVICE_CONTENT.get(slug)

    # SECONDARY: fallback cards
    fallback_service = find_fallback_service(slug)

    if not content and not fallback_service:
        raise Http404("Service not found")

    # BASIC SERVICE DATA
    if fallback_service:
        service_name = fallback_service["name"]
        category_name = fallback_service["category_name"]
    else:
        # fallback minimal
        service_name = slug.replace("-", " ").title()
        category_name = "Service"

    # CONTENT (100% from content.py)
    intro = content.get("intro", "") if content else ""
    sections = _build_sections(content or {})

    # GALLERY (collect from sections)
    gallery_images = []
    for sec in sections:
        for img in sec.get("images", []):
            gallery_images.append({
                "url": img,
                "alt": service_name
            })

    # LIMIT images (clean UI)
    gallery_images = gallery_images[:6]

    # META
    meta_title = f"{service_name} | Sudama Interiors"
    meta_description = intro or f"Explore professional {service_name.lower()} services with premium execution."

    return render(
        request,
        "services/service_detail.html",
        {
            "service": {
                "name": service_name,
                "category_name": category_name,
            },
            "hero_description": intro,
            "meta_title": meta_title,
            "meta_description": meta_description,
            "intro": intro,
            "detail_sections": sections,
            "gallery_images": gallery_images,
            "construction_layout": content.get("construction_layout") if content else None,
            "door_specs": content.get("door_specs") if content else None,
            "service_highlights": content.get("highlights", []) if content else [],
        },
    )