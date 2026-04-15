import hashlib

from django import template

register = template.Library()


def _stable_int(value: str) -> int:
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()
    return int(digest[:10], 16)


def _fallback_line(label: str) -> str:
    intents = (
        "streamlined daily operation",
        "lasting panel stability",
        "refined visible finish",
        "wear resistance in active zones",
        "clean detailing at installation",
        "consistent performance over time",
        "balanced form and utility",
        "precise fit during assembly",
    )
    templates = (
        "{label} is selected when projects need {intent}.",
        "For practical interiors, {label} delivers {intent}.",
        "Use {label} to maintain {intent} across repeated use.",
        "Teams specify {label} where spaces depend on {intent}.",
        "In finished joinery, {label} supports {intent}.",
        "Install {label} wherever design quality must meet {intent}.",
        "{label} helps interior elements retain {intent}.",
        "Choose {label} for applications that call for {intent}.",
    )

    seed = _stable_int(label.lower())
    intent = intents[seed % len(intents)]
    template_line = templates[(seed // len(intents)) % len(templates)]
    return template_line.format(label=label, intent=intent)


def _from_keywords(name: str) -> str:
    label = (name or "").strip() or "This material"
    lowered = label.lower()

    keyword_copy = (
        (("hinge",), "Engineered to keep shutters moving smoothly while preserving long-term alignment."),
        (("laminate",), "Adds a polished top layer that shields base boards from daily surface wear."),
        (("plywood",), "Chosen as a structural core where cabinets need reliable load-bearing strength."),
        (("mdf",), "Creates a uniform panel base that accepts routed profiles and painted finishes cleanly."),
        (("hdf",), "Its dense composition supports compact panel work that faces frequent contact."),
        (("veneer",), "Applies real wood character to fronts and panels with a lighter visual expression."),
        (("acrylic",), "Delivers mirror-like shutter faces that keep contemporary kitchens visually sharp."),
        (("membrane",), "Wraps profiled shutters in one skin for neat edges and moisture-safe daily use."),
        (("handle",), "Improves grip comfort and control in openings used repeatedly through the day."),
        (("channel",), "Keeps cabinetry handle-free while maintaining quick, intuitive drawer and shutter access."),
        (("lock",), "Protects storage contents with controlled access that remains easy to operate."),
        (("drawer", "slide"), "Maintains fluid drawer travel under load, reducing drag during routine operation."),
        (("edge", "band"), "Seals exposed board sides to reduce moisture entry and chipped finishing."),
        (("adhesive",), "Creates dependable inter-material bonding that holds layers together under stress."),
        (("fevicol",), "Trusted for board assembly where consistent glue strength supports clean joinery."),
        (("glass",), "Brings visual lightness to doors and partitions without sacrificing functional clarity."),
        (("mirror",), "Amplifies light throw and perceived depth in wardrobes, dressers, and compact rooms."),
        (("granite",), "Performs on heavy-use worktops by resisting heat, impact, and everyday abrasion."),
        (("quartz",), "Offers non-porous countertop performance with uniform tone and easy upkeep."),
        (("tile",), "Protects floors and walls with hardwearing coverage suited to moisture-prone zones."),
        (("stone",), "Introduces grounded texture where durability and long service life are core priorities."),
        (("wpc",), "Handles humid conditions without swelling, making it suitable for wet-area furniture."),
        (("pvc",), "Provides water-tolerant panel utility for bathrooms, utility spaces, and service areas."),
        (("aluminium",), "Combines light profile strength with corrosion resistance in long-use frame systems."),
        (("steel",), "Supports hardware and framework applications where higher rigidity is essential."),
    )

    for keywords, line in keyword_copy:
        if all(keyword in lowered for keyword in keywords):
            return line

    return _fallback_line(label)


@register.simple_tag
def product_microcopy(product):
    return _from_keywords(getattr(product, "name", ""))
