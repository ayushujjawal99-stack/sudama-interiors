from django.db import migrations, models


def curate_services(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    curated = [
        {
            "title": "Bespoke Residential Interiors",
            "slug": "bespoke-residential-interiors",
            "short_description": "Layered homes shaped with material warmth, intelligent planning, and a deeply personal design language.",
            "description": "We craft residences that feel composed, intimate, and quietly luxurious. Every space is planned around daily rituals, light, storage, movement, and tactile finishes so the final home feels effortless rather than decorated.",
            "image": "services/modular-solutions/modular-solutions_trending_1.jpg",
        },
        {
            "title": "Modular Kitchens",
            "slug": "modular-kitchens",
            "short_description": "Precision kitchens with premium shutters, refined lighting, ergonomic storage, and a showroom-level finish.",
            "description": "Our kitchen process balances visual drama with everyday performance. We plan work triangles, appliance flow, cabinetry, hardware, lighting, and surfaces as one integrated experience.",
            "image": "services/modular-solutions/modular-solutions_kitchen_1.jpg",
        },
        {
            "title": "Luxury Wardrobes and Storage",
            "slug": "luxury-wardrobes-storage",
            "short_description": "Elegant wardrobes, walk-ins, and concealed storage systems designed for calm, order, and premium tactility.",
            "description": "From sliding wardrobes to boutique walk-in rooms, we design storage that feels architectural. Finishes, lighting, handle profiles, mirrors, and internal organization are tuned to the client lifestyle.",
            "image": "services/modular-solutions/modular-solutions_wardrobe_1.jpg",
        },
        {
            "title": "False Ceiling and Lighting Design",
            "slug": "false-ceiling-lighting-design",
            "short_description": "Sculpted ceilings and layered lighting scenes that give rooms cinematic depth after sunset.",
            "description": "We shape ceiling profiles, coves, task lighting, accent light, and ambient glow to transform the emotional tone of a room. The result is practical by day and atmospheric by night.",
            "image": "services/false-ceiling/false-ceiling_designs_1.jpg",
        },
        {
            "title": "Space Planning and Layouts",
            "slug": "space-planning-layouts",
            "short_description": "Smart layouts that make compact, premium, and family spaces feel more fluid, beautiful, and usable.",
            "description": "Every strong interior begins with movement. We refine zoning, furniture scale, circulation, privacy, storage, and sightlines before finishes are selected, creating spaces that work before they impress.",
            "image": "services/layout-plans/layout-plans_floor_1.jpeg",
        },
        {
            "title": "Doors, Partitions and Feature Walls",
            "slug": "doors-partitions-feature-walls",
            "short_description": "Statement doors, elegant partitions, TV walls, and feature surfaces that add architectural polish.",
            "description": "We use doors, partitions, and vertical surfaces to create rhythm, privacy, and visual anchors. Materials are selected for proportion, durability, and the premium mood of the whole interior.",
            "image": "services/doors-windows/doors-windows_interior-doors_1.jpeg",
        },
    ]
    Service.objects.all().delete()
    for item in curated:
        Service.objects.update_or_create(slug=item["slug"], defaults=item)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_remove_contact_leads"),
        ("services", "0004_rename_services_se_service_790fa8_idx_services_se_service_dc9624_idx_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="ServiceImage"),
        migrations.DeleteModel(name="ServiceSection"),
        migrations.RemoveIndex(model_name="service", name="services_se_slug_4657d0_idx"),
        migrations.RemoveIndex(model_name="service", name="services_se_name_32d28c_idx"),
        migrations.RemoveField(model_name="service", name="category"),
        migrations.RemoveField(model_name="service", name="hero_images"),
        migrations.RemoveField(model_name="service", name="meta_description"),
        migrations.RemoveField(model_name="service", name="meta_title"),
        migrations.RemoveField(model_name="service", name="updated_at"),
        migrations.RemoveField(model_name="service", name="full_description"),
        migrations.RenameField(model_name="service", old_name="name", new_name="title"),
        migrations.RunPython(curate_services, migrations.RunPython.noop),
        migrations.AlterField(model_name="service", name="title", field=models.CharField(max_length=200)),
        migrations.AlterField(model_name="service", name="slug", field=models.SlugField(unique=True)),
        migrations.AlterField(model_name="service", name="short_description", field=models.TextField()),
        migrations.AlterField(model_name="service", name="description", field=models.TextField()),
        migrations.AlterField(model_name="service", name="image", field=models.ImageField(upload_to="services/")),
        migrations.AlterModelOptions(name="service", options={"ordering": ("title",)}),
        migrations.DeleteModel(name="ServiceCategory"),
    ]
