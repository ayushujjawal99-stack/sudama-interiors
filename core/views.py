# core/views.py
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import ContactLeadForm
from services.models import Service, ServiceCategory
from products.models import ProductCategory


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # All service categories + their services.
        # prefetch_related = 2 total DB queries, not N+1.
        ctx['service_categories'] = (
            ServiceCategory.objects
            .prefetch_related('services')
            .order_by('name')
        )

        ctx['product_categories'] = (
            ProductCategory.objects
            .prefetch_related('products')
            .order_by('name')
        )

        return ctx


def contact(request):
    service_categories = ServiceCategory.objects.prefetch_related('services').all()
    product_categories = ProductCategory.objects.prefetch_related('products').all()

    context = {
        'service_categories': service_categories,
        'product_categories': product_categories,
    }

    return render(request, 'contact.html', context)

from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_admin(request):
    User = get_user_model()

    user, created = User.objects.get_or_create(username='admin')
    user.set_password('admin12345')   # ✅ THIS IS IMPORTANT
    user.is_staff = True
    user.is_superuser = True
    user.save()

    return HttpResponse("Admin reset done properly")
    