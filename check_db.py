import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'sudama.settings'
sys.path.insert(0, r'c:\Users\playd\sudama_interiors')
import django
django.setup()
from services.models import ServiceCategory, Service
print(f"Categories: {ServiceCategory.objects.count()}")
print(f"Services: {Service.objects.count()}")
for c in ServiceCategory.objects.all().order_by('name'):
    print(f"\n{c.name}:")
    for s in c.services.all():
        print(f"  - {s.name} [{s.slug}]")
