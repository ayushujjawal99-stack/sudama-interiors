import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'sudama.settings'
django.setup()
from services.models import ServiceCategory, Service
for c in ServiceCategory.objects.prefetch_related('services').order_by('name'):
    services = [f"{s.name} [{s.slug}]" for s in c.services.all()]
    print(f"\n{c.name}:")
    for s in services:
        print(f"  - {s}")
