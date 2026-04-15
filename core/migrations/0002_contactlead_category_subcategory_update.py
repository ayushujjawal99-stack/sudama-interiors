from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0003_alter_service_options"),
        ("core", "0001_contactlead"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contactlead",
            old_name="full_name",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="contactlead",
            old_name="phone_number",
            new_name="phone",
        ),
        migrations.RemoveField(
            model_name="contactlead",
            name="service_interest",
        ),
        migrations.AddField(
            model_name="contactlead",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contact_leads",
                to="services.servicecategory",
            ),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="subcategory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contact_leads",
                to="services.service",
            ),
        ),
    ]
