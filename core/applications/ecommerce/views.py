from django.shortcuts import render
from django.views.generic import ListView
from core.applications.ecommerce.models import Product


# Create your views here.
class ListProductView(ListView):
    model = Product
    template_name = "ecommerce/product_list.html"
