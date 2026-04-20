from django.core.management.base import BaseCommand
from services.models import ServiceCategory, Service


class Command(BaseCommand):
    help = "Seed service categories and services from business data"

    def handle(self, *args, **options):
        data = {
            "Interiors": [
                ("Modular Solutions", "Factory-finished interior systems for fast installation and high customization."),
                ("False Ceiling", "Premium false ceiling solutions for lighting, aesthetics, and acoustic performance."),
                ("ACP Cladding", "Durable and modern surface solution for exterior facades and interior applications."),
                ("Curtains & Blinds", "Window treatments combining functionality with aesthetics — Zebra, Roller, and Enrich Shade blinds."),
            ],
            "Doors & Windows": [
                ("Doors & Windows", "Complete range of interior and exterior doors with precise material, size, and finish specifications."),
            ],
            "Construction": [
                ("Construction", "From planning to technical layouts — floor plans, 3D visualization, vastu integration, electrical and plumbing layouts."),
                ("Iron / Metal Fabrication", "Custom iron and metal fabrication for shades, roofing structures, and iron foundations."),
            ],
        }

        created_cats = 0
        created_services = 0

        for cat_name, services in data.items():
            cat, created = ServiceCategory.objects.get_or_create(name=cat_name)
            if created:
                created_cats += 1
                self.stdout.write(f"  Created category: {cat_name}")

            for name, desc in services:
                svc, created = Service.objects.get_or_create(
                    name=name,
                    defaults={
                        "category": cat,
                        "description": desc,
                        "short_description": desc,
                    },
                )
                if created:
                    created_services += 1
                    self.stdout.write(f"    Created service: {name} [{svc.slug}]")
                else:
                    # Update description if service already exists
                    svc.description = desc
                    svc.short_description = desc
                    svc.save()

        self.stdout.write(self.style.SUCCESS(
            f"\nDone: {created_cats} categories, {created_services} services created."
        ))
