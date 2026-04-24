from django.http import Http404
from django.shortcuts import render
from django.views import View

from core.site_content import (
    fallback_product_cards,
    find_fallback_product,
    find_fallback_product_category,
    product_card_from_model,
    product_groups_from_queryset,
)
from .models import ProductCategory, Product


# ============================= #
# SAFE NORMALIZER
# ============================= #
def _safe(val):
    return (val or "").strip().lower()


# ============================= #
# CATEGORY CONTENT (PREMIUM)
# ============================= #
def _category_sections(category):
    name = (category.get("name") if isinstance(category, dict) else (category.name or "")).strip()
    key = _safe(name)

    handcrafted = {
        "Curtain": {
            "intro": "Curtain systems shape how a space feels—controlling light, privacy, and softness with precision. The right fabric and fall can elevate a room without overpowering it.",
            "includes": "Blackout drapes, sheers, layered combinations, stitched panels, track systems, and hardware tailored to room conditions.",
            "where_used": "Bedrooms, living areas, offices, lounges, and glazing-heavy spaces where light and privacy need careful balance.",
            "why_matters": "A well-chosen curtain system reduces glare, improves comfort, and completes the visual language of the space.",
            "choose_us_points": [
                "Fabric selection aligned with light, privacy, and maintenance.",
                "Clean stitching and fall for a controlled, premium look.",
                "Practical guidance across styles and budgets.",
                "Execution from measurement to final installation.",
            ],
        },
        "Frames": {
            "intro": "Frame systems define alignment and structural clarity for doors, partitions, and openings.",
            "includes": "Door frames, partition frames, profile systems across materials and finishes.",
            "where_used": "Doors, partitions, enclosures, and transition points within interiors.",
            "why_matters": "Accurate framing ensures long-term alignment, stability, and finish consistency.",
            "choose_us_points": [
                "Precision measurement and planning.",
                "Material selection based on load and environment.",
                "Clean installation with alignment control.",
                "Durable performance over time.",
            ],
        },
        "Hardware": {
            "intro": "Hardware determines how smoothly a space functions—every movement, closure, and adjustment depends on it.",
            "includes": "Hinges, locks, handles, channels, and motion systems.",
            "where_used": "Doors, cabinets, drawers, and modular furniture.",
            "why_matters": "Good hardware ensures reliability, reduces wear, and improves everyday usability.",
            "choose_us_points": [
                "Right hardware for usage intensity.",
                "Smooth operation with long cycle life.",
                "Compatibility with materials and design.",
                "Accurate fitting and alignment.",
            ],
        },
        "Laminates": {
            "intro": "Laminates define the visible surface quality—color, texture, and reflection shape the perception of the entire space.",
            "includes": "Gloss, matte, textured, and specialty laminates.",
            "where_used": "Cabinets, wardrobes, panels, and furniture fronts.",
            "why_matters": "They protect the base material while delivering a consistent, durable finish.",
            "choose_us_points": [
                "Finish curation based on lighting and usage.",
                "Edge detailing and joint consistency.",
                "Surface durability and maintenance guidance.",
                "Application precision for clean outcomes.",
            ],
        },
        "Panels & Louvers": {
            "intro": "Panels and louvers introduce depth, rhythm, and visual layering without clutter.",
            "includes": "Decorative wall panels, fluted systems, louvers in wood and composite finishes.",
            "where_used": "Feature walls, partitions, and accent zones.",
            "why_matters": "They create focal points while maintaining a controlled design language.",
            "choose_us_points": [
                "Layout planning for visual balance.",
                "Material selection for durability and finish.",
                "Precision installation for alignment.",
                "Integration with lighting and furniture.",
            ],
        },
        "Plywood": {
            "intro": "Plywood is the structural backbone of interior work, defining strength, stability, and longevity.",
            "includes": "MR, BWR, BWP, calibrated and marine-grade boards.",
            "where_used": "Furniture carcasses, kitchens, wardrobes, and partitions.",
            "why_matters": "Correct grade selection prevents failure, improves load handling, and extends life.",
            "choose_us_points": [
                "Grade selection based on moisture and usage.",
                "Structural planning for durability.",
                "Compatibility with laminates and finishes.",
                "Execution aligned with real site conditions.",
            ],
        },
        "UV Sheets": {
            "intro": "UV sheets deliver high-gloss, mirror-like finishes for contemporary interiors.",
            "includes": "High-gloss panels and UV-coated surfaces.",
            "where_used": "Wardrobes, shutters, and modern furniture systems.",
            "why_matters": "They create a clean, reflective finish while maintaining surface durability.",
            "choose_us_points": [
                "Finish selection aligned with lighting.",
                "Careful handling to avoid surface damage.",
                "Clean edge detailing and alignment.",
                "Consistent installation quality.",
            ],
        },
    }

    for k in handcrafted:
        if _safe(k) == key:
            return handcrafted[k]

    return {
        "intro": f"{name} contributes to both performance and finish quality across interior systems.",
        "includes": f"This category includes multiple material options under {name}.",
        "where_used": f"{name} is used across residential and commercial interiors.",
        "why_matters": f"Correct selection improves durability, usability, and long-term consistency.",
        "choose_us_points": [
            "Practical selection based on real usage.",
            "Material compatibility and finish control.",
            "Execution aligned with site conditions.",
            "Long-term performance focus.",
        ],
    }


# ============================= #
# PRODUCT CONTENT (PREMIUM)
# ============================= #
def _product_sections(product):
    name = (product.get("name") if isinstance(product, dict) else (product.name or "")).strip()
    key = _safe(name)

    handcrafted = {
        "mr": {
            "intro": "MR plywood is a practical base choice for dry interior applications where cost efficiency and structural stability are priorities.",
            "what_it_is": "Moisture-resistant plywood designed for low-humidity environments.",
            "where_used": "Wardrobes, beds, storage units, and general furniture.",
            "why_it_matters": "Delivers reliable performance for indoor use without unnecessary cost escalation.",
            "choose_us_points": [
                "Correct grade selection based on usage.",
                "Clean fabrication for structural stability.",
                "Execution aligned with design intent.",
                "Balanced cost-performance approach.",
            ],
        },
        "bwr": {
            "intro": "BWR plywood offers a balanced solution for areas exposed to moderate moisture.",
            "what_it_is": "Boiling water resistant plywood for semi-moist conditions.",
            "where_used": "Kitchen cabinets, storage units, and utility zones.",
            "why_it_matters": "Reduces the risk of swelling and extends furniture life compared to MR grade.",
            "choose_us_points": [
                "Material planning based on environment.",
                "Joint strength and durability focus.",
                "Cost vs performance optimization.",
                "Reliable execution standards.",
            ],
        },
        "bwp": {
            "intro": "BWP plywood is engineered for high-moisture environments where long-term durability is critical.",
            "what_it_is": "Boiling water proof plywood suitable for wet areas.",
            "where_used": "Kitchen sink units, bathrooms, and utility areas.",
            "why_it_matters": "Prevents warping, swelling, and structural degradation over time.",
            "choose_us_points": [
                "Grade selection for wet zones.",
                "Durability-focused installation.",
                "Quality checks during execution.",
                "Long-term performance assurance.",
            ],
        },
        "mica": {
            "intro": "Mica laminates define the visible finish of interiors, balancing aesthetics with protection.",
            "what_it_is": "Decorative laminate applied over base boards.",
            "where_used": "Wardrobes, cabinets, panels, and furniture surfaces.",
            "why_it_matters": "Enhances durability while delivering a refined visual finish.",
            "choose_us_points": [
                "Finish selection based on design intent.",
                "Edge detailing and surface alignment.",
                "Clean lamination process.",
                "Consistent installation quality.",
            ],
        },
    }

    for k in handcrafted:
        if _safe(k) == key:
            return handcrafted[k]

    return {
        "intro": f"{name} supports both functional performance and finish quality in interior applications.",
        "what_it_is": f"{name} is used as part of structured interior systems.",
        "where_used": "Furniture, cabinetry, and interior panels.",
        "why_it_matters": "Improves usability, durability, and overall project quality.",
        "choose_us_points": [
            "Material selection based on actual usage.",
            "Execution aligned with design intent.",
            "Balanced performance and cost.",
            "Long-term reliability focus.",
        ],
    }


# ============================= #
# PRODUCTS HOME
# ============================= #
class ProductsHomeView(View):
    def get(self, request):
        groups = product_groups_from_queryset(
            ProductCategory.objects.prefetch_related("products").order_by("name")
        )
        return render(request, "products/products_home.html", {
            "product_groups": groups or fallback_product_cards()
        })


# ============================= #
# CATEGORY VIEW
# ============================= #
class ProductCategoryView(View):
    def get(self, request, category_slug):
        category = ProductCategory.objects.prefetch_related("products").filter(slug=category_slug).first()

        if category:
            category_data = product_groups_from_queryset([category])[0]
        else:
            category_data = find_fallback_product_category(category_slug)

        if not category_data:
            raise Http404("Product category not found")

        context = {"category": category_data}
        context.update(_category_sections(category_data))
        return render(request, "products/category_detail.html", context)


# ============================= #
# PRODUCT DETAIL
# ============================= #
class ProductDetailView(View):
    def get(self, request, category_slug, product_slug):
        product = Product.objects.select_related("category").filter(
            category__slug=category_slug,
            slug=product_slug
        ).first()

        if product:
            product_data = product_card_from_model(product)
            category_data = product_groups_from_queryset([product.category])[0]
        else:
            category_data, product_data = find_fallback_product(category_slug, product_slug)

        if not product_data:
            raise Http404("Product not found")

        context = {
            "category": category_data,
            "product": product_data,
        }

        context.update(_product_sections(product_data))
        return render(request, "products/product_detail.html", context)