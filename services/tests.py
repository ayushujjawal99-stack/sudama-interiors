from django.test import TestCase
from django.urls import reverse

from .models import Service, ServiceCategory


class ServiceModelTests(TestCase):
    def test_slug_is_generated_on_save(self):
        category = ServiceCategory.objects.create(name="Interiors")

        service = Service.objects.create(
            category=category,
            name="False Ceiling",
            short_description="Premium false ceiling solutions.",
        )

        self.assertEqual(service.slug, "false-ceiling")


class ServiceDetailViewTests(TestCase):
    def test_service_detail_renders_with_related_services(self):
        category = ServiceCategory.objects.create(name="Construction")
        service = Service.objects.create(
            category=category,
            name="Borewell / Boring",
            short_description="Reliable borewell work.",
        )
        related = Service.objects.create(
            category=category,
            name="Iron Fabrication",
            short_description="Custom metal fabrication.",
        )

        response = self.client.get(
            reverse("services:service_detail", kwargs={"slug": service.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, service.name)
        self.assertContains(response, related.name)
