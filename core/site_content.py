from django.urls import reverse


FALLBACK_SERVICE_GROUPS = [
    {
        "name": "Interiors",
        "summary": (
            "Design-led interior services for homes, offices, and commercial spaces, "
            "planned around comfort, storage, light, and long-term finish quality."
        ),
        "services": [
            {
                "name": "Modular Solutions",
                "slug": "modular-solutions",
                "short_description": "Factory-finished kitchens, wardrobes, TV units, storage, and office systems.",
                "full_description": (
                    "Modular solutions bring speed, accuracy, and dependable finish quality to everyday interiors. "
                    "Each system is planned around usage, storage flow, material durability, and site dimensions."
                ),
            },
            {
                "name": "False Ceiling",
                "slug": "false-ceiling",
                "short_description": "Clean ceiling systems for lighting design, concealed services, and premium room depth.",
                "full_description": (
                    "False ceiling work improves visual hierarchy, lighting control, acoustics, and service concealment "
                    "while keeping the room elegant and easy to maintain."
                ),
            },
            {
                "name": "ACP Cladding",
                "slug": "acp-cladding",
                "short_description": "Durable interior and exterior cladding for modern facades and feature surfaces.",
                "full_description": (
                    "ACP cladding gives buildings and interior surfaces a sharp, low-maintenance finish with strong "
                    "weather resistance and clean contemporary detailing."
                ),
            },
        ],
    },
    {
        "name": "Doors & Windows",
        "summary": (
            "Well-fitted access, ventilation, and daylight systems built for durability, alignment, security, and finish."
        ),
        "services": [
            {
                "name": "Doors & Windows",
                "slug": "doors-windows",
                "short_description": "Interior and exterior doors, windows, frames, hardware, and finish systems.",
                "full_description": (
                    "Doors and windows shape how a space opens, breathes, receives light, and stays secure. "
                    "We plan materials, sizes, hardware, and finish details for dependable daily use."
                ),
            },
        ],
    },
    {
        "name": "Construction",
        "summary": (
            "Site-aware construction support covering planning, foundations, layouts, water systems, and utility execution."
        ),
        "services": [
            {
                "name": "Construction Foundation Plans",
                "slug": "construction-foundation-plans",
                "short_description": "Foundation, reinforcement, concreting, waterproofing, and structural support works.",
                "full_description": (
                    "Foundation planning protects the long-term strength of a project through soil-aware, load-aware, "
                    "and execution-ready structural decisions."
                ),
            },
            {
                "name": "Layout Plans",
                "slug": "layout-plans",
                "short_description": "2D layouts, 3D planning, vastu integration, and MEP coordination.",
                "full_description": (
                    "Layout planning connects design intent with practical execution so rooms, utilities, circulation, "
                    "and construction teams work from a clear shared direction."
                ),
            },
            {
                "name": "Submersible & Handpump",
                "slug": "submersible-handpump",
                "short_description": "Reliable water access through pump installation, handpump setup, and plumbing layouts.",
                "full_description": (
                    "Water systems are planned around dependable access, correct pump selection, safe piping, and "
                    "serviceability for long-term use."
                ),
            },
        ],
    },
]


FALLBACK_PRODUCT_GROUPS = [
    {
        "name": "Plywood",
        "slug": "plywood",
        "summary": "Structural board materials for durable cabinetry, wardrobes, kitchens, and custom furniture.",
        "image": "images/products/plywood.png",
        "products": [
            {"name": "MR", "slug": "mr", "description": "Moisture resistant plywood for dry interior furniture."},
            {"name": "BWR", "slug": "bwr", "description": "Boiling water resistant plywood for stronger day-to-day durability."},
            {"name": "BWP", "slug": "bwp", "description": "Boiling water proof plywood for wet and demanding zones."},
        ],
    },
    {
        "name": "Laminates",
        "slug": "laminates",
        "summary": "Decorative surfaces that protect boards while defining the visible finish language of interiors.",
        "image": "images/products/laminates.png",
        "products": [
            {"name": "Mica", "slug": "mica", "description": "Durable laminate finish for everyday cabinetry and panels."},
            {"name": "Acrylic Laminates", "slug": "acrylic-laminates", "description": "Glossy, premium fronts for modern kitchens and wardrobes."},
            {"name": "PVC Laminates", "slug": "pvc-laminates", "description": "Water-tolerant laminate surfaces for active utility spaces."},
        ],
    },
    {
        "name": "Hardware",
        "slug": "hardware",
        "summary": "High-touch fittings that make doors, drawers, shutters, and storage systems work smoothly.",
        "image": "images/products/hardware.png",
        "products": [
            {"name": "Hinges", "slug": "hinges", "description": "Movement hardware for aligned, smooth shutters."},
            {"name": "Channels", "slug": "channels", "description": "Handle-free profile systems for clean storage fronts."},
            {"name": "Door handles & Locks", "slug": "door-handles-locks", "description": "Comfortable access hardware with reliable security."},
        ],
    },
    {
        "name": "Panels & Louvers",
        "slug": "panels-louvers",
        "summary": "Feature wall, furniture, and cladding surfaces that add rhythm, depth, and visual refinement.",
        "image": "images/products/panels-louvers.png",
        "products": [
            {"name": "Decorative Panels", "slug": "decorative-panels", "description": "Feature surfaces for walls and furniture faces."},
            {"name": "Linear Louvers", "slug": "linear-louvers", "description": "Vertical or horizontal profile systems for depth and rhythm."},
        ],
    },
    {
        "name": "Curtain",
        "slug": "curtain",
        "summary": "Soft furnishing solutions for privacy, daylight control, warmth, and finished room character.",
        "image": "images/products/curtain.png",
        "products": [
            {"name": "Blackout Curtains", "slug": "blackout-curtains", "description": "Light control for bedrooms and media spaces."},
            {"name": "Sheer Curtains", "slug": "sheer-curtains", "description": "Soft daylight filtering for living spaces and lounges."},
        ],
    },
    {
        "name": "UV Sheets",
        "slug": "uv-sheets",
        "summary": "Bright, high-gloss decorative sheets for polished modern furniture and visible fronts.",
        "image": "images/products/uv-sheets.png",
        "products": [
            {"name": "High Gloss UV Sheets", "slug": "high-gloss-uv-sheets", "description": "Reflective finish sheets for contemporary cabinetry."},
        ],
    },
]


def service_url(slug):
    return reverse("services:service_detail", kwargs={"slug": slug})


def product_category_url(slug):
    return reverse("products:category_detail", kwargs={"category_slug": slug})


def product_url(category_slug, product_slug):
    return reverse(
        "products:product_detail",
        kwargs={"category_slug": category_slug, "product_slug": product_slug},
    )


def fallback_service_cards():
    groups = []
    for group in FALLBACK_SERVICE_GROUPS:
        services = []
        for service in group["services"]:
            services.append(
                {
                    **service,
                    "category_name": group["name"],
                    "summary": service.get("short_description") or service.get("full_description"),
                    "url": service_url(service["slug"]),
                    "is_fallback": True,
                }
            )
        groups.append({**group, "services": services, "is_fallback": True})
    return groups


def fallback_product_cards():
    groups = []
    for group in FALLBACK_PRODUCT_GROUPS:
        products = []
        for product in group["products"]:
            products.append(
                {
                    **product,
                    "category_name": group["name"],
                    "category_slug": group["slug"],
                    "summary": product.get("description", ""),
                    "url": product_url(group["slug"], product["slug"]),
                    "is_fallback": True,
                }
            )
        groups.append(
            {
                **group,
                "url": product_category_url(group["slug"]),
                "products": products,
                "is_fallback": True,
            }
        )
    return groups


def service_card_from_model(service):
    return {
        "name": service.name,
        "slug": service.slug,
        "category_name": service.category.name if service.category_id else "",
        "short_description": service.short_description,
        "full_description": service.full_description,
        "summary": service.short_description or service.full_description,
        "url": service.get_absolute_url() if service.slug else reverse("services:services_home"),
        "model": service,
        "is_fallback": False,
    }


def service_groups_from_queryset(categories):
    groups = []
    for category in categories:
        services = [service_card_from_model(service) for service in category.services.all()]
        if services:
            groups.append(
                {
                    "name": category.name,
                    "summary": "",
                    "services": services,
                    "model": category,
                    "is_fallback": False,
                }
            )
    return groups


def product_card_from_model(product):
    category = product.category
    category_slug = category.slug or ""
    return {
        "name": product.name,
        "slug": product.slug,
        "category_name": category.name,
        "category_slug": category_slug,
        "description": product.description,
        "summary": product.description,
        "url": product.get_absolute_url() if product.slug and category_slug else reverse("products:products_home"),
        "model": product,
        "is_fallback": False,
    }


def product_groups_from_queryset(categories):
    groups = []
    for category in categories:
        products = [product_card_from_model(product) for product in category.products.all()]
        slug = category.slug or ""
        groups.append(
            {
                "name": category.name,
                "slug": slug,
                "summary": "Curated material options selected for finish quality, durability, and daily performance.",
                "image": f"images/products/{slug}.png" if slug else "",
                "url": category.get_absolute_url() if slug else reverse("products:products_home"),
                "products": products,
                "model": category,
                "is_fallback": False,
            }
        )
    return groups


def find_fallback_service(slug):
    for group in fallback_service_cards():
        for service in group["services"]:
            if service["slug"] == slug:
                return {**service, "category_summary": group.get("summary", "")}
    return None


def find_fallback_product_category(slug):
    for group in fallback_product_cards():
        if group["slug"] == slug:
            return group
    return None


def find_fallback_product(category_slug, product_slug):
    category = find_fallback_product_category(category_slug)
    if not category:
        return None, None
    for product in category["products"]:
        if product["slug"] == product_slug:
            return category, product
    return category, None
