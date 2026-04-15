from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:110] or "category"
            slug = base_slug
            suffix = 2
            while ProductCategory.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug[:105]}-{suffix}"
                suffix += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:category_detail", kwargs={"category_slug": self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:160] or "product"
            slug = base_slug
            suffix = 2
            while Product.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug[:155]}-{suffix}"
                suffix += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "products:product_detail",
            kwargs={
                "category_slug": self.category.slug,
                "product_slug": self.slug,
            },
        )

    def __str__(self):
        return self.name