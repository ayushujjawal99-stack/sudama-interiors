from django.urls import reverse, NoReverseMatch


# =========================
# SAFE URL HANDLER
# =========================
def safe_reverse(name, kwargs=None):
    try:
        return reverse(name, kwargs=kwargs or {})
    except NoReverseMatch:
        return "#"


# =========================
# FALLBACK DATA
# =========================

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
                    "Modular solutions bring speed, accuracy, and dependable finish quality to everyday interiors."
                ),
            },
            {
                "name": "False Ceiling",
                "slug": "false-ceiling",
                "short_description": "Clean ceiling systems for lighting design and premium room depth.",
                "full_description": (
                    "False ceiling improves visual hierarchy, lighting control, and service concealment."
                ),
            },
            {
                "name": "ACP Cladding",
                "slug": "acp-cladding",
                "short_description": "Durable cladding for modern facades and feature surfaces.",
                "full_description": (
                    "ACP cladding gives buildings a sharp, low-maintenance finish."
                ),
            },
        ],
    },
]


FALLBACK_PRODUCT_GROUPS = [
    {
        "name": "Plywood",
        "slug": "plywood",
        "summary": "Structural board materials for durable cabinetry and furniture.",
        "image": "images/products/plywood.png",
        "products": [
            {"name": "MR", "slug": "mr", "description": "Moisture resistant plywood."},
            {"name": "BWR", "slug": "bwr", "description": "Boiling water resistant plywood."},
        ],
    },
]


# =========================
# URL HELPERS
# =========================

def service_url(slug):
    return safe_reverse("services:service_detail", {"slug": slug})


def product_category_url(slug):
    return safe_reverse("products:category_detail", {"category_slug": slug})


def product_url(category_slug, product_slug):
    return safe_reverse(
        "products:product_detail",
        {"category_slug": category_slug, "product_slug": product_slug},
    )


# =========================
# FALLBACK BUILDERS
# =========================

def fallback_service_cards():
    groups = []

    for group in FALLBACK_SERVICE_GROUPS:
        services = []

        for service in group["services"]:
            services.append(
                {
                    "name": service["name"],
                    "slug": service["slug"],
                    "category_name": group["name"],
                    "summary": service.get("short_description") or service.get("full_description"),
                    "url": service_url(service["slug"]),
                    "is_fallback": True,
                }
            )

        groups.append(
            {
                "name": group["name"],
                "summary": group.get("summary", ""),
                "services": services,
                "is_fallback": True,
            }
        )

    return groups


def fallback_product_cards():
    groups = []

    for group in FALLBACK_PRODUCT_GROUPS:
        products = []

        for product in group["products"]:
            products.append(
                {
                    "name": product["name"],
                    "slug": product["slug"],
                    "category_name": group["name"],
                    "category_slug": group["slug"],
                    "summary": product.get("description", ""),
                    "url": product_url(group["slug"], product["slug"]),
                    "is_fallback": True,
                }
            )

        groups.append(
            {
                "name": group["name"],
                "slug": group["slug"],
                "summary": group.get("summary", ""),
                "image": group.get("image", ""),
                "url": product_category_url(group["slug"]),
                "products": products,
                "is_fallback": True,
            }
        )

    return groups


# =========================
# MODEL ADAPTERS
# =========================

def service_card_from_model(service):
    return {
        "name": service.name,
        "slug": service.slug,
        "category_name": service.category.name if service.category_id else "",
        "summary": service.short_description or service.full_description or "",
        "url": service.get_absolute_url() if service.slug else safe_reverse("services:services_home"),
        "is_fallback": False,
    }


def service_groups_from_queryset(categories):
    groups = []

    for category in categories:
        services = [service_card_from_model(s) for s in category.services.all()]

        if services:
            groups.append(
                {
                    "name": category.name,
                    "summary": "",
                    "services": services,
                    "is_fallback": False,
                }
            )

    return groups


def product_card_from_model(product):
    category = product.category

    return {
        "name": product.name,
        "slug": product.slug,
        "category_name": category.name if category else "",
        "category_slug": category.slug if category else "",
        "summary": product.description or "",
        "url": product.get_absolute_url() if product.slug else safe_reverse("products:products_home"),
        "is_fallback": False,
    }


def product_groups_from_queryset(categories):
    groups = []

    for category in categories:
        products = [product_card_from_model(p) for p in category.products.all()]

        groups.append(
            {
                "name": category.name,
                "slug": category.slug or "",
                "summary": "Curated material options selected for durability and finish quality.",
                "image": f"images/products/{category.slug}.png" if category.slug else "",
                "url": category.get_absolute_url() if category.slug else safe_reverse("products:products_home"),
                "products": products,
                "is_fallback": False,
            }
        )

    return groups