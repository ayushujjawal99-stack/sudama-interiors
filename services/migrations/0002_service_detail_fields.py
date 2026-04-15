from django.db import migrations, models
from django.utils.text import slugify


def populate_service_detail_fields(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    for service in Service.objects.all().order_by("id"):
        base_slug = slugify(service.name) or "service"
        slug = base_slug
        suffix = 1

        while Service.objects.exclude(pk=service.pk).filter(slug=slug).exists():
            suffix += 1
            slug = f"{base_slug}-{suffix}"

        description = (service.description or "").strip()
        meta_description = description[:252].strip()
        if meta_description and len(description) > 252:
            meta_description = f"{meta_description}..."

        service.slug = slug
        service.short_description = description
        service.meta_title = f"{service.name} | Sudama Interiors"
        service.meta_description = meta_description or (
            f"Explore premium {service.name.lower()} services by Sudama Interiors."
        )
        service.save(
            update_fields=(
                "slug",
                "short_description",
                "meta_title",
                "meta_description",
            )
        )


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="full_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="service",
            name="meta_description",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="service",
            name="meta_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="service",
            name="short_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="service",
            name="slug",
            field=models.SlugField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.RunPython(populate_service_detail_fields, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="service",
            name="slug",
            field=models.SlugField(unique=True),
        ),
    ]
