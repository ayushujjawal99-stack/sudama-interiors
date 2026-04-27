from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0005_service_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="hero_images",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
