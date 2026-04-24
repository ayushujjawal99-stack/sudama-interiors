from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# ============================= #
# CATEGORY
# ============================= #

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


# ============================= #
# SERVICE
# ============================= #

class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services'
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)

    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)

    # ✅ SAFE IMAGE FIELD
    image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True
    )

    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    # ✅ SAFE URL (NO CRASH IF ROUTE MISSING)
    def get_absolute_url(self):
        try:
            return reverse("services:service_detail", kwargs={"slug": self.slug})
        except:
            return "#"

    def save(self, *args, **kwargs):
        # ✅ ALWAYS GENERATE SAFE SLUG
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.name) or "service"
        slug = base_slug
        counter = 2

        while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug


# ============================= #
# SERVICE SECTION (Dynamic Content)
# ============================= #

class ServiceSection(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='sections'
    )

    title = models.CharField(max_length=200)
    content = models.TextField()

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=["service", "order"]),
        ]

    def __str__(self):
        return f"{self.service.name} - {self.title}"


# ============================= #
# SERVICE IMAGE (GALLERY)
# ============================= #

class ServiceImage(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='images'
    )

    # ✅ FIXED (NO 500 IF IMAGE NOT PROVIDED)
    image = models.ImageField(
        upload_to='services/gallery/',
        blank=True,
        null=True
    )

    alt_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.service.name} Image"