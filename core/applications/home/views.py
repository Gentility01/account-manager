from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from core.applications.ecommerce.models import Product, Category, ProductImages
from django.db.models.query import QuerySet
from typing import Optional

# Create your views here.


class HomeView(TemplateView):
    template_name = "pages/home.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = reverse_lazy(
        "login",
    )  # Assuming 'login' is the name of the login URL pattern

    def dispatch(self, request, *args, **kwargs):
        if not request.user.administrator_profile.exists():
            # If the user is not an administrator, redirect them to another page
            return redirect(
                reverse_lazy("not_administrator"),
            )
        # Assuming 'not_administrator' is the name of the URL pattern for the page
        return super().dispatch(request, *args, **kwargs)


class ProductShopListView(ListView):
    model = Product
    template_name = "pages/shop_lists.html"
    paginate_by = 8
    context_object_name = "all_products"

    def get_queryset(self):
        # Add ordering to the queryset
        return Product.objects.order_by('id')

    def get_context_data(self, **kwargs):
        """Add pagination context data."""
        context = super().get_context_data(**kwargs)
        context['page_obj'] = context['paginator'].page(context['page_obj'].number)  # Set page_obj
        return context


class ProductShopDetailView(DetailView):
    model = Product
    template_name = "pages/shop_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        images = ProductImages.objects.filter(product=product)
        context['product_images'] = images
        return context

class ProductsCategoryList(ListView):
    model = Product
    template_name = "pages/shop_by_category.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):
        # get the category base on the slug in the url
        category_slug = self.kwargs["category_slug"]
        category = Category.objects.get(slug=category_slug)
        queryset = Product.objects.filter(category=category).order_by("created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add category to the context for use in the template
        category_slug = self.kwargs['category_slug']
        category = Category.objects.get(slug=category_slug)
        context['category'] = category
        context['page_obj'] = context['paginator'].page(context['page_obj'].number)  # Set page_obj
        return context
