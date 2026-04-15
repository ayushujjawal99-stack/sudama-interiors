from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services'
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("services:service_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.name) or "service"
        slug = base_slug
        suffix = 1

        while Service.objects.exclude(pk=self.pk).filter(slug=slug).exists():
            suffix += 1
            slug = f"{base_slug}-{suffix}"

        return slug
