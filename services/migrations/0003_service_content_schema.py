import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0002_service_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="servicecategory",
            options={
                "ordering": ("name",),
                "verbose_name_plural": "Service Categories",
            },
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name="service",
                    name="description",
                ),
            ],
            database_operations=[],
        ),
        migrations.AddField(
            model_name="service",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="service",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="service",
            name="slug",
            field=models.SlugField(blank=True, max_length=170, unique=True),
        ),
        migrations.CreateModel(
            name="ServiceSection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sections",
                        to="services.service",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="ServiceImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="services/gallery/")),
                ("alt_text", models.CharField(blank=True, max_length=150)),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="services.service",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="service",
            index=models.Index(fields=["slug"], name="services_se_slug_4657d0_idx"),
        ),
        migrations.AddIndex(
            model_name="service",
            index=models.Index(fields=["name"], name="services_se_name_32d28c_idx"),
        ),
        migrations.AddIndex(
            model_name="servicesection",
            index=models.Index(
                fields=["service", "order"],
                name="services_se_service_790fa8_idx",
            ),
        ),
    ]
