from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactLead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("phone_number", models.CharField(max_length=20)),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "service_interest",
                    models.CharField(
                        choices=[
                            ("interior_design", "Interior Design"),
                            ("construction", "Construction"),
                            ("renovation", "Renovation"),
                            ("materials_products", "Materials / Products"),
                        ],
                        max_length=32,
                    ),
                ),
                ("message", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-created_at",)},
        ),
    ]
