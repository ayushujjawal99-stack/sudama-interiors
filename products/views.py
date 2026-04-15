# products/views.py
from django.views.generic import ListView, DetailView
from .models import ProductCategory, Product


class ProductsHomeView(ListView):
    template_name = 'products/products_home.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return (
            ProductCategory.objects
            .prefetch_related('products')
            .order_by('name')
        )


def _category_sections(category):
    name = category.name.strip()
    handcrafted = {
        "Curtain": {
            "intro": "Curtain materials define how a room feels through light control, privacy, and softness. This category supports both decorative layering and practical coverage. It helps interiors feel complete without visual heaviness.",
            "includes": "This category can include blackout options, sheers, textured drapes, stitched panel systems, and supporting accessories based on room requirement.",
            "where_used": "Commonly used in bedrooms, living rooms, office cabins, lounge areas, and glazing-heavy spaces that need comfort with controlled daylight.",
            "why_matters": "The right curtain selection improves ambience, reduces glare, supports privacy, and adds warmth to otherwise hard-surfaced interiors.",
            "choose_us_points": [
                "Fabric recommendations based on light, usage, and room character.",
                "Neat stitching and finish quality for a premium fall and drape.",
                "Practical selection support across style and maintenance needs.",
                "Reliable execution from planning to final installation.",
            ],
        },
        "Frames": {
            "intro": "Frame systems hold key interior and architectural elements in place with visual precision. This category focuses on profiles that combine strength and clean detailing. It supports both structural confidence and finished appearance.",
            "includes": "Depending on project scope, this can include door frames, partition frames, profile systems, trim supports, and utility frame assemblies.",
            "where_used": "Used in door openings, partition layouts, glass enclosures, modular furniture boundaries, and transition points between wall and joinery.",
            "why_matters": "Well-built frames improve alignment, support long-term fit, and prevent finishing issues that usually appear when foundational support is weak.",
            "choose_us_points": [
                "Dimension-accurate frame planning for cleaner final fit.",
                "Material selection matched to load and environment.",
                "Execution quality focused on line consistency and stability.",
                "Dependable site coordination for smoother installation flow.",
            ],
        },
        "Hardware": {
            "intro": "Hardware brings motion, grip, and control to interior components that users touch every day. This category covers the functional layer that makes furniture and doors feel dependable. It is essential for long-term usability.",
            "includes": "Includes hinges, channels, slides, locks, handles, connectors, and other fittings that support opening, closing, and secure operation.",
            "where_used": "Applied across kitchens, wardrobes, bathroom storage, doors, modular systems, and custom furniture in both residential and commercial spaces.",
            "why_matters": "Good hardware improves movement quality, lowers maintenance issues, and keeps fitted components aligned through repeated daily cycles.",
            "choose_us_points": [
                "Application-based hardware matching for lasting performance.",
                "Installation accuracy that protects smooth movement.",
                "Specification support balancing comfort, function, and budget.",
                "Execution reliability with consistent quality checks.",
            ],
        },
        "Laminates": {
            "intro": "Laminate materials shape the visible finish language of an interior while protecting base boards underneath. This category combines aesthetics with practical surface performance. It is central to modern cabinetry and panel work.",
            "includes": "Can include matte and glossy laminates, textured sheets, decorative surfaces, and functional variants selected for different room conditions.",
            "where_used": "Used on kitchen shutters, wardrobes, storage fronts, wall cladding panels, furniture tops, and interior joinery faces.",
            "why_matters": "A suitable laminate system improves stain resistance, keeps cleaning simple, and helps visual themes stay consistent across multiple rooms.",
            "choose_us_points": [
                "Finish curation based on usage, lighting, and design intent.",
                "Precise application workflows for long-lasting surface behavior.",
                "Edge detailing standards that improve overall visual quality.",
                "Reliable guidance from sample selection to completion.",
            ],
        },
        "Panels & Louvers": {
            "intro": "Panels and louvers add depth, rhythm, and controlled texture to walls and furniture faces. This category is used when interiors need a refined design statement with practical build compatibility. It bridges aesthetics and function.",
            "includes": "May include decorative panels, linear louvers, fluted profiles, acoustic-friendly options, and cladding-ready systems for feature surfaces.",
            "where_used": "Widely applied in TV backdrops, bedroom feature walls, reception zones, corridor highlights, and selected modular furniture elevations.",
            "why_matters": "It helps define focal points, improves spatial character, and upgrades plain surfaces into intentional design elements.",
            "choose_us_points": [
                "Design-aligned panel planning for balanced visual composition.",
                "Installation precision that preserves line continuity.",
                "Material choices suited to maintenance and durability goals.",
                "Execution support tailored to project finish standards.",
            ],
        },
        "Plywood": {
            "intro": "Plywood forms the structural backbone of most interior furniture and joinery systems. This category focuses on board grades chosen for strength, stability, and long service life. It is where functional durability begins.",
            "includes": "This can include MR, BWR, BWP, and other grade-specific boards selected according to moisture exposure and load requirements.",
            "where_used": "Used in kitchen carcasses, wardrobes, loft units, bed frames, storage systems, panel bases, and custom interior furniture.",
            "why_matters": "Right plywood selection prevents early deformation, improves screw-holding performance, and supports better finish outcomes over time.",
            "choose_us_points": [
                "Grade recommendations based on actual site conditions.",
                "Fabrication methods that protect board integrity.",
                "Build quality controls for stronger furniture life.",
                "Clear execution process from cutting to installation.",
            ],
        },
        "UV Sheets": {
            "intro": "UV sheets are chosen when interiors need a sharp reflective look with fast cleanability. This category supports contemporary design language while keeping surface upkeep practical. It is ideal for visible premium fronts.",
            "includes": "Can include high-gloss UV-coated boards, decorative finish sheets, and front-facing panel options tuned for modern interior palettes.",
            "where_used": "Typically used on wardrobes, kitchen shutters, vertical panel highlights, display units, and feature furniture fronts.",
            "why_matters": "They provide a sleek premium finish, maintain visual brightness, and simplify routine maintenance in high-visibility areas.",
            "choose_us_points": [
                "Finish selection guidance for cohesive contemporary styling.",
                "Surface-safe handling and installation standards.",
                "Detailing quality that avoids mismatch across panel sets.",
                "Dependable delivery for polished final presentation.",
            ],
        },
    }
    if name in handcrafted:
        return handcrafted[name]
    return {
        "intro": f"{name} represents a focused material category used to improve how interiors perform and look in everyday use. It supports both practical planning and better finish outcomes across different project types.",
        "includes": f"This category can include multiple product options under {name}, selected to match function, design direction, and durability needs.",
        "where_used": f"{name} materials are generally used in homes, offices, modular setups, and custom interior zones where performance and finish must stay balanced.",
        "why_matters": f"Choosing the right {name} solution helps improve usability, maintainability, and long-term quality in completed interiors.",
        "choose_us_points": [
            "Practical category guidance based on room and usage needs.",
            "Material selection support with clear functional reasoning.",
            "Execution quality focused on finish consistency.",
            "Reliable project handling from planning through delivery.",
        ],
    }


def _product_sections(product):
    name = product.name.strip()
    handcrafted = {
        "Acrylic Laminates": {
            "intro": "Acrylic Laminates are selected when you want a crisp, modern surface that stays visually clean in daily use. They give shutters a reflective finish that instantly brightens the room. In active homes, they balance style with practical wipe-and-go maintenance.",
            "what_it_is": "Acrylic laminate is a decorative surface sheet with a glossy top layer applied on board panels. In simple terms, it is what gives cabinets and wardrobes that smooth, mirror-like front.",
            "where_used": "Most commonly used on kitchen shutters, wardrobe doors, loft panels, and display furniture where a premium polished look is expected.",
            "why_it_matters": "It helps interiors look sharper, reduces effort in routine cleaning, and keeps visible surfaces consistent even with frequent touch and handling.",
            "choose_us_points": [
                "Finish-focused panel selection for a uniform gloss outcome.",
                "Precise edge detailing that avoids patchy visual breaks.",
                "Skilled installation workflow for clean front-line alignment.",
                "Reliable execution support from sampling to final fitting.",
            ],
        },
        "BWP": {
            "intro": "BWP is preferred for spaces where moisture exposure is part of normal use, especially around sinks and utility zones. It forms a strong base that stays stable under damp conditions. This makes it a dependable choice for long-life cabinetry.",
            "what_it_is": "BWP means Boiling Water Proof grade plywood designed for high moisture resistance. It is the core material used when furniture needs stronger protection against water impact.",
            "where_used": "Used in kitchen carcasses, sink units, utility cabinets, bathroom-adjacent storage, and service counters where humidity is persistent.",
            "why_it_matters": "It supports structural life in demanding zones, lowers risk of warping, and protects the finish from premature failures caused by moisture.",
            "choose_us_points": [
                "Correct grade recommendation based on actual usage conditions.",
                "Joinery methods that preserve board strength over time.",
                "Execution standards tuned for wet-area durability.",
                "Clear quality checks before and during installation.",
            ],
        },
        "BWR": {
            "intro": "BWR is ideal when interiors need reliable moisture resistance without moving into heavy-duty wet-zone specifications. It offers a practical balance between performance and budget. For most residential furniture, it delivers dependable day-to-day stability.",
            "what_it_is": "BWR stands for Boiling Water Resistant plywood, built to handle moderate moisture exposure. It is commonly chosen as a practical structural board for general interior furniture.",
            "where_used": "Applied in wardrobes, bedroom furniture, study units, living room storage, and dry kitchen sections requiring stronger longevity than basic grades.",
            "why_it_matters": "It improves furniture life, keeps panel behavior predictable, and helps maintain finish quality through changing seasonal conditions.",
            "choose_us_points": [
                "Material planning that matches product grade to usage zone.",
                "Neat fabrication with attention to load-bearing joints.",
                "Balanced specification guidance for cost and durability.",
                "Consistent on-site execution with dependable follow-through.",
            ],
        },
        "Channels": {
            "intro": "Channels are used to create clean, handle-free storage lines while keeping access easy and comfortable. They help modern interiors feel uncluttered without sacrificing daily usability. In compact spaces, they also reduce visual noise.",
            "what_it_is": "A channel is a profile system fitted into shutters or drawer lines to enable grip without external handles. It allows opening movement while preserving a minimal front elevation.",
            "where_used": "Installed in contemporary kitchens, wardrobes, utility cabinets, vanity units, and media consoles where straight-line design is preferred.",
            "why_it_matters": "It improves user comfort, keeps layouts visually lighter, and supports a more seamless finish language across full-height storage units.",
            "choose_us_points": [
                "Exact profile selection for smooth hand movement and aesthetics.",
                "Fine alignment control across long shutter runs.",
                "Installation precision that preserves linear consistency.",
                "Execution reliability for contemporary handle-less systems.",
            ],
        },
        "Door handles & Locks": {
            "intro": "Door handles and locks shape both convenience and security in everyday movement through a space. The right set feels natural in hand while still giving dependable control. They are small components with a major user experience impact.",
            "what_it_is": "This includes handle hardware for opening and lock systems for controlled access. In simple terms, these fittings determine how comfortably and securely doors are used.",
            "where_used": "Used on main doors, bedroom entries, bathroom doors, utility access points, and selected storage areas requiring privacy or restricted entry.",
            "why_it_matters": "Good hardware improves grip comfort, supports smoother operation cycles, and prevents early wear that usually appears in high-touch locations.",
            "choose_us_points": [
                "Ergonomic hardware options matched to door type and usage.",
                "Reliable locking systems selected for practical safety needs.",
                "Clean fitting standards for stable and silent operation.",
                "Execution discipline that avoids misalignment and rework.",
            ],
        },
        "Hinges": {
            "intro": "Hinges define how smoothly shutters move, close, and hold alignment over years of use. A well-selected hinge setup makes furniture feel refined in everyday interaction. It is a core performance layer behind visual cabinetry quality.",
            "what_it_is": "A hinge is the movement joint that connects shutters to cabinet bodies. It controls opening angle, closing behavior, and long-term door stability.",
            "where_used": "Found in kitchen shutters, wardrobe doors, overhead cabinets, bathroom vanities, and storage units that open multiple times a day.",
            "why_it_matters": "It protects shutter alignment, improves user comfort, and reduces maintenance issues caused by sagging, friction, or uneven closure.",
            "choose_us_points": [
                "Hinge selection based on shutter weight and opening frequency.",
                "Precise boring and mounting for balanced movement control.",
                "Adjustment-focused installation to maintain long-term fit.",
                "Quality-first execution across complete cabinetry systems.",
            ],
        },
        "MR": {
            "intro": "MR grade is a practical base choice for interior areas that stay mostly dry during regular use. It supports clean furniture execution where water contact is limited. For many standard rooms, it offers efficient and stable performance.",
            "what_it_is": "MR stands for Moisture Resistant plywood, intended for interior dry applications. It is a commonly used board for furniture that does not face persistent damp exposure.",
            "where_used": "Used in wardrobes, bedroom units, study tables, paneling, loft storage, and living room furniture in low-moisture zones.",
            "why_it_matters": "It provides dependable structural behavior for dry interiors while helping keep project specifications aligned with practical budget planning.",
            "choose_us_points": [
                "Application-led grade planning to avoid over or under specification.",
                "Careful board handling and fabrication for cleaner output.",
                "Well-controlled installation process for consistent panel behavior.",
                "Project guidance focused on value and execution quality.",
            ],
        },
        "Mica": {
            "intro": "Mica is chosen when surfaces need a neat finish with robust day-to-day practicality. It offers broad design flexibility across colors and textures while remaining easy to maintain. This makes it a strong option for active household furniture.",
            "what_it_is": "Mica is a decorative laminate sheet applied over plywood or board surfaces. In simple terms, it is the visible finishing layer that defines look, touch, and surface behavior.",
            "where_used": "Applied on kitchen shutters, wardrobes, storage fronts, wall panels, table tops, and custom furniture that need durable finish coverage.",
            "why_it_matters": "It improves stain resistance, protects base boards from surface wear, and allows interior themes to stay visually consistent across rooms.",
            "choose_us_points": [
                "Finish selection support across textures, tones, and use cases.",
                "Edge and joint detailing for cleaner visual continuity.",
                "Accurate lamination workflow to prevent bubbling or mismatch.",
                "Dependable delivery from sampling through final installation.",
            ],
        },
        "PVC Laminates": {
            "intro": "PVC Laminates are selected where moisture safety and low-maintenance surfaces are equally important. They help keep panels looking neat even in utility-heavy spaces. For practical interiors, they offer resilient finish performance with simple upkeep.",
            "what_it_is": "PVC laminate is a polymer-based surface layer used on boards for protective finishing. It acts as a shield that supports water tolerance and routine cleanability.",
            "where_used": "Typically used in kitchens, utility cabinets, bathroom-adjacent furniture, service counters, and storage units that face regular cleaning cycles.",
            "why_it_matters": "It reduces moisture-related surface stress, keeps maintenance straightforward, and preserves finish quality in spaces with frequent contact.",
            "choose_us_points": [
                "Usage-specific surface recommendations for wet and active zones.",
                "Installation quality focused on stable adhesion and clean edges.",
                "Execution checks that protect long-term finish durability.",
                "Reliable coordination from selection to on-site completion.",
            ],
        },
    }

    if name in handcrafted:
        return handcrafted[name]

    # Keep a unique, readable fallback for any newly added products.
    return {
        "intro": f"{name} is selected to improve day-to-day performance while preserving a refined interior finish. It supports practical use, cleaner detailing, and reliable long-term behavior after installation.",
        "what_it_is": f"{name} is a core interior product used to strengthen how furniture or finishes perform in real spaces. In simple terms, it helps turn design intent into dependable execution.",
        "where_used": f"{name} is generally applied in kitchens, wardrobes, storage systems, and custom furniture where finish clarity and functional consistency are important.",
        "why_it_matters": f"Using {name} thoughtfully improves durability, simplifies maintenance, and helps interior elements hold their intended quality through regular use.",
        "choose_us_points": [
            "Material recommendations aligned to actual usage and finish intent.",
            "Execution standards focused on accuracy, fit, and clean detailing.",
            "Practical guidance to balance performance goals with project budget.",
            "Reliable delivery support from selection through final installation.",
        ],
    }


class ProductCategoryView(DetailView):
    model = ProductCategory
    template_name = "products/category_detail.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "category_slug"

    def get_queryset(self):
        return ProductCategory.objects.prefetch_related("products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        context["meta_title"] = f"{category.name} | Product Category | Sudama Interiors"
        context["meta_description"] = (
            f"Explore the {category.name} category at Sudama Interiors with applications, benefits, "
            f"and material options for practical and premium spaces."
        )
        context.update(_category_sections(category))
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "product_slug"

    def get_queryset(self):
        return Product.objects.select_related("category").filter(
            category__slug=self.kwargs.get("category_slug")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        section_copy = _product_sections(product)
        context["meta_title"] = f"{product.name} | Sudama Interiors"
        context["meta_description"] = (
            f"Explore {product.name} from Sudama Interiors with practical guidance on usage, "
            f"benefits, finish outcomes, and long-term performance."
        )
        context.update(section_copy)
        return context