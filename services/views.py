from django.shortcuts import get_object_or_404, render

from .models import Service, ServiceCategory


def _build_fallback_content(service):
    service_name = service.name
    category_name = service.category.name
    service_lower = service_name.lower()

    fallback_paragraphs = [
        (
            f"{service_name} is designed for clients who want {category_name.lower()} work "
            f"that feels refined, durable, and deeply aligned with the way they live or work. "
            f"At Sudama Interiors, we approach every {service_lower} project as a balance of "
            f"design clarity, practical performance, and long-term value."
        ),
        (
            f"Our team studies the layout, usage patterns, lighting conditions, material "
            f"compatibility, and finishing requirements before shaping a {service_lower} "
            f"solution. This helps us create spaces that are not only visually premium, but "
            f"also efficient to maintain and comfortable in day-to-day use."
        ),
        (
            f"We work with dependable materials, trusted fabrication partners, and detail-led "
            f"execution standards so the final {service_lower} result looks polished from every "
            f"angle. From substrate quality to visible finishes, every layer is selected to "
            f"support strength, consistency, and a clean final appearance."
        ),
        (
            f"Our process begins with design consultation and requirement discovery, followed "
            f"by planning, measurements, detailing, and coordinated execution. This structured "
            f"workflow allows us to deliver {service_lower} work with fewer site issues, tighter "
            f"quality control, and clear communication at every stage."
        ),
        (
            f"Clients choose our {service_lower} service because it combines customization with "
            f"professional discipline. Whether the requirement is modern, timeless, minimal, or "
            f"luxury-focused, we tailor the detailing, finish palette, and installation approach "
            f"to match the larger design language of the property."
        ),
        (
            f"Beyond aesthetics, we focus on durability, workmanship, and finish retention over "
            f"time. The result is a {service_lower} solution that elevates the experience of the "
            f"space today while continuing to perform beautifully in the years ahead."
        ),
    ]

    process_steps = [
        {
            "step": "Design",
            "title": f"{service_name} Discovery",
            "description": (
                f"We understand your goals, style references, site limitations, and functional "
                f"expectations before shaping the right {service_lower} direction."
            ),
        },
        {
            "step": "Planning",
            "title": "Technical Planning",
            "description": (
                f"Our team prepares measurements, material selections, execution details, and "
                f"coordination checkpoints to keep the {service_lower} scope clear and efficient."
            ),
        },
        {
            "step": "Execution",
            "title": "Crafted Delivery",
            "description": (
                f"Fabrication, installation, and finishing are carried out with close supervision "
                f"so every {service_lower} detail meets our quality standards."
            ),
        },
        {
            "step": "Delivery",
            "title": "Final Handover",
            "description": (
                f"We complete final inspections, finishing touch-ups, and quality review so your "
                f"{service_lower} solution is ready for confident use."
            ),
        },
    ]

    service_highlights = [
        f"Tailored {service_lower} solutions that suit your space, style, and usage needs",
        "Premium material selection with strong focus on finish quality and longevity",
        "Detail-oriented planning that reduces on-site delays and execution errors",
        "Skilled workmanship with clean finishing, accurate alignment, and durable results",
        "Professional project coordination from consultation to final handover",
        "A premium brand approach that prioritizes aesthetics, reliability, and value",
    ]

    return fallback_paragraphs, process_steps, service_highlights


def services_home(request):
    categories = (
        ServiceCategory.objects.prefetch_related("services").order_by("name")
    )
    return render(
        request,
        "services/services_home.html",
        {
            "categories": categories,
        },
    )


def service_detail(request, slug):
    service = get_object_or_404(
        Service.objects.select_related("category"),
        slug=slug,
    )
    related_services = (
        Service.objects.select_related("category")
        .filter(category=service.category)
        .exclude(pk=service.pk)
        .order_by("name")[:4]
    )
    fallback_paragraphs, process_steps, service_highlights = _build_fallback_content(service)

    full_description_paragraphs = [
        paragraph.strip()
        for paragraph in service.full_description.splitlines()
        if paragraph.strip()
    ]

    hero_description = (
        service.short_description
        or service.description
        or f"Premium {service.name.lower()} solutions designed and executed with craftsmanship, precision, and lasting quality."
    )
    meta_title = service.meta_title or f"{service.name} | Sudama Interiors"
    meta_description = (
        service.meta_description
        or service.short_description
        or service.description
        or f"Explore premium {service.name.lower()} services by Sudama Interiors, delivered with tailored design, quality materials, and precise execution."
    )

    return render(
        request,
        "services/service_detail.html",
        {
            "service": service,
            "hero_description": hero_description,
            "meta_title": meta_title,
            "meta_description": meta_description,
            "content_paragraphs": full_description_paragraphs or fallback_paragraphs,
            "process_steps": process_steps,
            "service_highlights": service_highlights,
            "related_services": related_services,
        },
    )

from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_admin(request):
    User = get_user_model()
    User.objects.all().delete()

    User.objects.create_superuser(
        username='admin',
        email='admin@gmail.com',
        password='admin12345'
    )

    return HttpResponse("Admin recreated")
