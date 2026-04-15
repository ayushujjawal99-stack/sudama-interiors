from django import template

register = template.Library()


def _service_blurb_from_name(service_name, category_name):
    name = (service_name or "").lower()
    category = (category_name or "").lower()

    keyword_blurbs = (
        (("false ceiling",), "Refines ceiling depth while improving lighting balance and finish definition."),
        (("modular", "solutions"), "Brings organized planning and flexible storage into everyday living spaces."),
        (("wardrobe",), "Creates efficient storage with a finish that feels seamless in the room."),
        (("storage",), "Adds practical organization without disturbing the visual calm of the space."),
        (("kitchen",), "Improves workflow, storage access, and the overall finish of daily cooking spaces."),
        (("living room",), "Shapes a welcoming setting that feels composed, comfortable, and well-resolved."),
        (("bedroom",), "Supports comfort and quiet through thoughtful detailing, textures, and layout decisions."),
        (("bathroom",), "Balances moisture-safe materials with a cleaner, more polished everyday experience."),
        (("office",), "Improves focus and efficiency with better planning, storage, and ergonomic comfort."),
        (("door",), "Strengthens access points while improving fit, finish, and long-term performance."),
        (("window",), "Enhances light, ventilation, and durability with better-built framed openings."),
        (("cladding",), "Adds a sharp external finish with durable material protection and visual consistency."),
        (("fabrication",), "Delivers structural support through precise metalwork built for lasting use."),
        (("borewell", "boring"), "Secures dependable water access with site-aware drilling and technical care."),
        (("submersible",), "Supports stable water movement with reliable installation and serviceability."),
        (("handpump",), "Provides practical water access where durability and everyday function matter most."),
        (("painting",), "Refreshes surfaces with cleaner coverage, stronger preparation, and longer finish life."),
        (("flooring",), "Improves underfoot durability while giving the room a more complete visual base."),
        (("electrical",), "Supports safe day-to-day usage through planned wiring, load balance, and neat execution."),
        (("plumbing",), "Keeps essential water systems efficient, durable, and easier to maintain over time."),
    )

    for keywords, blurb in keyword_blurbs:
        if all(keyword in name for keyword in keywords):
            return blurb

    if "interior" in category:
        return "Shapes comfort, usability, and visual harmony with a more considered design approach."
    if "construction" in category:
        return "Focuses on dependable execution, structural strength, and work that holds up over time."
    return "Supports the project with a practical, well-finished solution tailored to the space."


@register.simple_tag
def service_microcopy(service):
    short_description = (getattr(service, "short_description", "") or "").strip()
    if short_description:
        return short_description

    description = (getattr(service, "description", "") or "").strip()
    if description:
        return description

    return _service_blurb_from_name(
        getattr(service, "name", ""),
        getattr(getattr(service, "category", None), "name", ""),
    )


@register.simple_tag
def category_copy(category):
    category_name = (getattr(category, "name", "") or "").strip().lower()

    if category_name == "interiors":
        return (
            "Our interior services are designed to make spaces feel more complete, personal, "
            "and comfortable in everyday use. We focus on layout clarity, material balance, "
            "lighting, storage, and finishing details that quietly improve how a room performs. "
            "The result is not just visual appeal, but a living environment that feels calmer, "
            "more functional, and more aligned with your lifestyle."
        )

    if category_name == "construction":
        return (
            "Our construction services support the strength behind the finished space, with close "
            "attention to execution quality, technical accuracy, and long-term durability. We work "
            "with a practical site-led approach so structural tasks, utility systems, and finishing "
            "support elements are handled with discipline. This helps ensure the project performs "
            "reliably, not just during handover, but through everyday use over time."
        )

    return (
        "Each service in this category is planned to support the project with a balance of design "
        "clarity, dependable execution, and a finish that feels intentional in the larger space."
    )


@register.simple_tag
def listing_transition_copy():
    return (
        "Good spaces are not built by design alone. Once the interior direction is clear, the "
        "project depends on accurate execution, structural discipline, and technical reliability "
        "to carry that vision into a finished result."
    )
