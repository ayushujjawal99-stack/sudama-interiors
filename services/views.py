from django.shortcuts import get_object_or_404, render
from .models import Service, ServiceCategory


# 🔥 FIXED CONTENT MAP (BEST FOR YOUR CASE)
SERVICE_CONTENT = {
    "acp-cladding": {
        "what_it_is": "ACP cladding is a modern exterior and interior surface solution that provides durability, weather resistance, and a premium architectural finish.",
        "types": [
            "Exterior ACP cladding",
            "Interior ACP panels",
            "Facade cladding systems",
        ],
        "features": [
            "Weather resistant and long-lasting",
            "Lightweight yet strong panels",
            "Modern premium appearance",
        ],
        "specifications": [
            "Material: Aluminum composite panels",
            "Finish: Matte / Gloss / Metallic",
        ],
        "usage": "Used in building facades, commercial spaces, and modern interiors.",
    },

    "doors-windows": {
        "what_it_is": "Doors and windows define access, ventilation, and aesthetics while ensuring safety and comfort in a space.",
        "types": [
            "Sliding doors & windows",
            "Casement systems",
            "Fixed glass panels",
        ],
        "features": [
            "Strong structural build",
            "Sound insulation options",
            "Weather resistance",
        ],
        "specifications": [
            "Material: Wood / Aluminum / uPVC",
            "Finish: Powder coating / Laminate",
        ],
        "usage": "Used in homes, offices, balconies, and commercial buildings.",
    },

    "false-ceiling": {
        "what_it_is": "False ceilings enhance aesthetics while improving lighting, insulation, and overall ceiling design.",
        "types": [
            "Gypsum ceilings",
            "POP ceilings",
            "PVC ceilings",
            "Wooden ceilings",
        ],
        "features": [
            "Improves lighting design",
            "Conceals wiring and ducts",
            "Enhances interior aesthetics",
        ],
        "specifications": [
            "Material: Gypsum / POP / PVC / Wood",
            "Finish: Paint / Texture / Laminates",
        ],
        "usage": "Used in living rooms, bedrooms, offices, and commercial interiors.",
    },

    "modular-solutions": {
        "what_it_is": "Modular solutions are factory-made units designed for flexibility, fast installation, and modern living.",
        "types": [
            "Modular kitchens",
            "Wardrobes",
            "TV units",
            "Storage units",
        ],
        "features": [
            "Quick installation",
            "Customizable designs",
            "Modern clean finish",
        ],
        "specifications": [
            "Material: MDF / Plywood / HDF",
            "Finish: Laminate / Acrylic / PU",
        ],
        "usage": "Used in homes, offices, and commercial spaces for efficient space utilization.",
    },
}


# 🔶 HOME
def services_home(request):
    categories = ServiceCategory.objects.prefetch_related("services").order_by("name")
    return render(request, "services/services_home.html", {
        "categories": categories,
    })


# 🔶 DETAIL
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

    # 🔥 MAIN FIX HERE
    content = SERVICE_CONTENT.get(slug, {
        "what_it_is": "Premium interior solution designed for modern spaces.",
        "types": [],
        "features": [],
        "specifications": [],
        "usage": "",
    })

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

        # 🔥 STRUCTURED DATA
        "what_it_is": content["what_it_is"],
        "types": content["types"],
        "features": content["features"],
        "specifications": content["specifications"],
        "usage": content["usage"],

        "service_highlights": [
            "Premium material quality",
            "Clean finishing standards",
            "Durable and long-lasting",
            "Modern design compatibility",
        ],

        "related_services": related_services,
    })