from django.db import migrations, models
from django.utils.text import slugify


def populate_category_slugs(apps, schema_editor):
    ProductCategory = apps.get_model("products", "ProductCategory")
    used = set()

    for category in ProductCategory.objects.all().order_by("id"):
        base_slug = slugify(category.name or "")[:110] or "category"
        slug = base_slug
        suffix = 2

        while slug in used or ProductCategory.objects.exclude(pk=category.pk).filter(slug=slug).exists():
            slug = f"{base_slug[:105]}-{suffix}"
            suffix += 1

        category.slug = slug
        category.save(update_fields=["slug"])
        used.add(slug)


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_product_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="productcategory",
            name="slug",
            field=models.SlugField(blank=True, max_length=120, null=True, unique=True),
        ),
        migrations.RunPython(populate_category_slugs, migrations.RunPython.noop),
    ]
