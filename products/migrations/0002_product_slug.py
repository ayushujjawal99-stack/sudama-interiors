from django.db import migrations, models
from django.utils.text import slugify


def populate_product_slugs(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    used = set()

    for product in Product.objects.all().order_by("id"):
        base_slug = slugify(product.name or "")[:160] or "product"
        slug = base_slug
        suffix = 2

        while slug in used or Product.objects.exclude(pk=product.pk).filter(slug=slug).exists():
            slug = f"{base_slug[:155]}-{suffix}"
            suffix += 1

        product.slug = slug
        product.save(update_fields=["slug"])
        used.add(slug)


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, max_length=170, null=True, unique=True),
        ),
        migrations.RunPython(populate_product_slugs, migrations.RunPython.noop),
    ]
