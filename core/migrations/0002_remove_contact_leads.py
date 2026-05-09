from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        ("services", "0004_rename_services_se_service_790fa8_idx_services_se_service_dc9624_idx_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="ContactLead"),
    ]
