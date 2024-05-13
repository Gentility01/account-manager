from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.applications.ecommerce.models import Product, Category, Tags
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from core.applications.ecommerce.forms import ProductForm, CategoryForm, TagsForm
from core.applications.users.models import ContentManager
from django.http import HttpResponseForbidden
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

# Create your views here.

# class CanCRUDProductMixin(PermissionRequiredMixin):
#     permission_required = 'ecommerce.can_crud_product'
#     login_url = reverse_lazy('account_login')

#     def has_permission(self):
#         if super().has_permission():
#             user = self.request.user
#             return user.is_superuser or user.groups.filter(name='ContentManager').exists()
#         return False


class ContentManagerRequiredMixin(LoginRequiredMixin):
    """
    A mixin that only allows access to content managers.
    """
    def dispatch(self, request, *args, **kwargs):
        if not self.user_is_content_manager(request.user):
            return HttpResponseForbidden("You don't have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

    def user_is_content_manager(self, user):
        """
        Checks if the user is a content manager.
        """
        return ContentManager.objects.filter(user=user).exists()


class AddCategoryView(ContentManagerRequiredMixin, CreateView):
    """
    A view for adding a new category.
    """
    model = Category
    form_class = CategoryForm
    template_name = "pages/ecommerce/add_category.html"
    success_url = reverse_lazy("ecommerce:list_category")


class ListCategoryView(ContentManagerRequiredMixin, ListView):
    """
    A view for listing all categories.
    """
    model = Category
    template_name = "pages/ecommerce/category_list.html"
    paginate_by = 5

    def get_queryset(self):
        return Category.objects.annotate(total_products=Count('product')).order_by("-created_at")

class EditCategoryView(ContentManagerRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "pages/ecommerce/edit_category.html"  
    success_url = reverse_lazy("ecommerce:list_category")

class DeleteCategoryView(ContentManagerRequiredMixin, DeleteView):
    model = Category
    template_name = "pages/ecommerce/delete_category.html"  
    success_url = reverse_lazy("ecommerce:list_category")

# -------------------------------------------------------------------------------------- Category views ends here --------------------------------------------------------------------------------------

class ListProductView(ContentManagerRequiredMixin, ListView):
    """
    A view for listing all products.
    """
    model = Product
    template_name = "pages/ecommerce/product_list.html"
    paginate_by = 5


class AddProductView(ContentManagerRequiredMixin, CreateView):
    """
    A view for adding a new product.
    """
    model = Product
    form_class = ProductForm
    template_name = "pages/ecommerce/add_product.html"
    success_url = reverse_lazy("ecommerce:list_product")


class EditProductView(ContentManagerRequiredMixin, UpdateView):
    """
    A view for editing an existing product.
    """
    model = Product
    form_class = ProductForm
    template_name = "pages/ecommerce/edit_product.html"
    success_url = reverse_lazy("users:dashboard_view:")


class DeleteProductView(ContentManagerRequiredMixin, DeleteView):
    """
    A view for deleting an existing product.    
    """
    model = Product
    template_name = "pages/ecommerce/delete_product.html"
    success_url = reverse_lazy("users:dashboard_view:")


class ProductDetailView(ContentManagerRequiredMixin, ListView):
    """
    A view for listing all products.
    """
    model = Product
    template_name = "ecommerce/product_detail.html"




# -------------------------------------------------------------------------------------- Product views ends here --------------------------------------------------------------------------------------


class CreateProductTags(ContentManagerRequiredMixin, CreateView):
    model = Tags
    form_class = TagsForm
    template_name = "pages/ecommerce/tags_create.html"
    success_url = reverse_lazy("ecommerce:list_tags")


class EditProductTags(ContentManagerRequiredMixin, UpdateView):
    model = Tags
    form_class = TagsForm
    template_name = "pages/ecommerce/tags_create.html"
    success_url = reverse_lazy("ecommerce:list_tags")

class DeleteProductTags(ContentManagerRequiredMixin, DeleteView):
    model = Tags
    form_class = TagsForm
    template_name = "pages/ecommerce/tags_delete.html"
    success_url = reverse_lazy("ecommerce:list_tags")


class ListProductTags(ContentManagerRequiredMixin, ListView):
    model = Tags
    form_class = TagsForm
    template_name = "pages/ecommerce/tags_list.html"
    paginate_by = 5


# -------------------------------------------------------------------------------------- Tag views ends here --------------------------------------------------------------------------------------     




        

    



    