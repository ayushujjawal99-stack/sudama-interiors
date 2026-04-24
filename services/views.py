from django.http import Http404
from django.shortcuts import render

from core.site_content import (
    fallback_service_cards,
    service_groups_from_queryset,
)
from .content import SERVICE_CONTENT
from .models import ServiceCategory


# ============================= #
# SERVICES HOME
# ============================= #

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
# SAFE SECTION BUILDER
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
# SERVICE DETAIL (FIXED)
# ============================= #

def service_detail(request, slug):
    # =============================
    # 1. GET SERVICE FROM DB PIPELINE
    # =============================
    categories = ServiceCategory.objects.prefetch_related("services")
    groups = service_groups_from_queryset(categories)

    all_services = [
        s for g in groups for s in g.get("services", [])
    ]

    service = next((s for s in all_services if s["slug"] == slug), None)

    # =============================
    # 2. FALLBACK (IF NOT FOUND)
    # =============================
    if not service:
        fallback_groups = fallback_service_cards()

        all_services = [
            s for g in fallback_groups for s in g.get("services", [])
        ]

        service = next((s for s in all_services if s["slug"] == slug), None)

    if not service:
        raise Http404("Service not found")

    # =============================
    # 3. CONTENT (FROM content.py)
    # =============================
    content = SERVICE_CONTENT.get(slug, {})

    intro = content.get("intro", "")
    sections = _build_sections(content)

    # =============================
    # 4. GALLERY BUILD
    # =============================
    gallery_images = []

    for sec in sections:
        for img in sec.get("images", []):
            gallery_images.append({
                "url": img,
                "alt": service["name"]
            })

    gallery_images = gallery_images[:6]

    # =============================
    # 5. META
    # =============================
    meta_title = f"{service['name']} | Sudama Interiors"
    meta_description = (
        intro
        or f"Explore professional {service['name'].lower()} services with premium execution."
    )

    # =============================
    # 6. RENDER
    # =============================
    return render(
        request,
        "services/service_detail.html",
        {
            "service": service,
            "hero_description": intro,
            "meta_title": meta_title,
            "meta_description": meta_description,
            "intro": intro,
            "detail_sections": sections,
            "gallery_images": gallery_images,
            "construction_layout": content.get("construction_layout"),
            "door_specs": content.get("door_specs"),
            "service_highlights": content.get("highlights", []),
        },
    )