import random

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
            "order": index,
        })

    return sections


def _section_images(content):
    images = []

    for section in content.get("sections", []):
        for image in section.get("images", []):
            if image and image not in images:
                images.append(image)

    return images


def _global_hero_pool(current_slug):
    images = []

    for slug, content in SERVICE_CONTENT.items():
        if slug == current_slug:
            continue

        source_images = content.get("hero_images") or _section_images(content)

        for image in source_images:
            if image and image not in images:
                images.append(image)

    return images


def _build_hero_images(slug, content, service_name, model_hero_images=None):
    service_images = set(_section_images(content))
    curated_images = [
        image for image in (model_hero_images or content.get("hero_images", []))
        if image and image not in service_images
    ]

    if len(curated_images) >= 3:
        hero_urls = curated_images[:3]
    else:
        fallback_pool = _global_hero_pool(slug)
        randomizer = random.Random(slug)
        randomizer.shuffle(fallback_pool)
        hero_urls = curated_images[:]

        for image in fallback_pool:
            if image not in hero_urls:
                hero_urls.append(image)
            if len(hero_urls) == 3:
                break

    return [
        {
            "url": image,
            "alt": f"{service_name} premium project view {index}",
        }
        for index, image in enumerate(hero_urls[:3], start=1)
    ]


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
    # 4. IMAGE SOURCES
    # =============================
    hero_images = _build_hero_images(
        slug,
        content,
        service["name"],
        service.get("hero_images"),
    )
    content_images = _section_images(content)

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
            "hero_images": hero_images,
            "content_images": content_images,
            "construction_layout": content.get("construction_layout"),
            "door_specs": content.get("door_specs"),
            "service_highlights": content.get("highlights", []),
        },
    )
