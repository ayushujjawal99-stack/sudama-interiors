from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductsHomeView.as_view(), name='products_home'),
    path('<slug:category_slug>/', views.ProductCategoryView.as_view(), name='category_detail'),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]