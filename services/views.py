from django.shortcuts import get_object_or_404, render
from .models import Service, ServiceCategory


# 🔥 FIXED CONTENT MAP (BEST FOR YOUR CASE)
SERVICE_CONTENT = {

    "acp-cladding": {
        "what_it_is": "ACP cladding is a modern architectural solution used for both exterior and interior surfaces, offering durability, weather resistance, and a sleek contemporary finish.",
        "types": [
            "Exterior ACP Cladding",
            "Interior ACP Panels",
            "Facade Cladding Systems",
            "Column & Feature Wall Cladding",
        ],
        "features": [
            "High weather resistance for long-term durability",
            "Lightweight panels with strong structural performance",
            "Modern metallic and matte finish options",
            "Corrosion and UV resistant surface",
        ],
        "specifications": [
            "Material: Aluminum Composite Panel",
            "Thickness: 3mm – 6mm",
            "Finish: Matte / Gloss / Metallic / Wooden",
        ],
        "usage": "Used in building facades, showrooms, offices, and modern interior feature walls where durability and visual impact are important.",
    },

    "doors-windows": {
        "what_it_is": "Doors and windows are essential structural elements that control access, ventilation, lighting, and security while enhancing the overall look of a space.",
        "types": [
            "Sliding Doors & Windows",
            "Casement Systems",
            "Fixed Glass Panels",
            "Flush Doors",
            "Aluminum & uPVC Systems",
        ],
        "features": [
            "Strong and durable build quality",
            "Sound insulation for improved comfort",
            "Weather-resistant for exterior applications",
            "Smooth operation and long-lasting fittings",
        ],
        "specifications": [
            "Material: Wood / Aluminum / uPVC / Glass",
            "Frame Thickness: Standard to Heavy Duty",
            "Finish: Powder Coating / Laminate / Polish",
        ],
        "usage": "Used in residential homes, offices, balconies, and commercial buildings for controlled access, ventilation, and aesthetics.",
    },

    "false-ceiling": {
        "what_it_is": "False ceilings are secondary ceiling systems designed to improve lighting, hide wiring, and enhance the aesthetic appeal of interior spaces.",
        "types": [
            "Gypsum Ceiling",
            "POP (Plaster of Paris) Ceiling",
            "PVC Ceiling",
            "Wooden Ceiling",
            "Grid Ceiling",
        ],
        "features": [
            "Enhances lighting and ambiance",
            "Conceals wiring, ducts, and pipes",
            "Improves thermal insulation",
            "Creates premium layered ceiling designs",
        ],
        "specifications": [
            "Material: Gypsum / POP / PVC / Wood",
            "Finish: Paint / Texture / Laminate",
            "Design: Plain / Cove / Layered / Patterned",
        ],
        "usage": "Used in living rooms, bedrooms, offices, showrooms, and commercial interiors to enhance ceiling design and lighting layout.",
    },

    "modular-solutions": {
        "what_it_is": "Modular solutions are factory-built interior units designed for efficiency, flexibility, and modern aesthetics, allowing faster installation and clean finishing.",
        "types": [
            "Modular Kitchens",
            "Wardrobes",
            "TV Units",
            "Storage Units",
            "Office Modular Systems",
        ],
        "features": [
            "Highly customizable layouts and finishes",
            "Fast installation with minimal site work",
            "Modern clean and premium appearance",
            "Efficient space utilization",
        ],
        "specifications": [
            "Material: MDF / Plywood / HDF",
            "Finish: Laminate / Acrylic / PU / Glass",
            "Hardware: Soft-close fittings and premium accessories",
        ],
        "usage": "Used in residential homes, apartments, offices, and commercial spaces for organized storage and modern interior setups.",
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