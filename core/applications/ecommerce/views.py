from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView

from core.applications.ecommerce.forms import CategoryForm
from core.applications.ecommerce.forms import ProductForm
from core.applications.ecommerce.forms import ProductImagesForm
from core.applications.ecommerce.forms import ProductReviewForm
from core.applications.ecommerce.forms import TagsForm
from core.applications.ecommerce.models import Category
from core.applications.ecommerce.models import Product
from core.applications.ecommerce.models import ProductImages
from core.applications.ecommerce.models import ProductReview
from core.applications.ecommerce.models import Tags
from core.applications.users.models import ContentManager


class ContentManagerRequiredMixin(LoginRequiredMixin):
    """
    A mixin that only allows access to content managers.
    """

    def dispatch(self, request, *args, **kwargs):
        if not self.user_is_content_manager(request.user):
            return HttpResponseForbidden(
                "You don't have permission to access this page.",
            )
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
    paginate_by = 10

    def get_queryset(self):
        return Category.objects.annotate(total_products=Count("product")).order_by(
            "-created_at",
        )


class EditCategoryView(ContentManagerRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "pages/ecommerce/edit_category.html"
    success_url = reverse_lazy("ecommerce:list_category")


class DeleteCategoryView(ContentManagerRequiredMixin, DeleteView):
    model = Category
    template_name = "pages/ecommerce/delete_category.html"
    success_url = reverse_lazy("ecommerce:list_category")


# ---------------------- Category views ends here ----------------


class ProductImagesCreateView(ContentManagerRequiredMixin, FormView):
    template_name = "pages/ecommerce/create_product_image.html"
    form_class = ProductImagesForm
    success_url = reverse_lazy("ecommerce:list_product_images")

    def form_valid(self, form):
        product = form.cleaned_data["product"]
        for each in self.request.FILES.getlist("image"):
            ProductImages.objects.create(image=each, product=product)
        return super().form_valid(form)


class ListProductImages(ContentManagerRequiredMixin, ListView):
    model = ProductImages
    template_name = "pages/ecommerce/list_product_imges.html"
    paginate_by = 10


class UpdateProductImages(ContentManagerRequiredMixin, UpdateView):
    model = ProductImages
    form_class = ProductImagesForm  # Use form_class instead of forms
    template_name = "pages/ecommerce/create_product_image.html"
    success_url = reverse_lazy("ecommerce:list_product_images")

    def form_valid(self, form):
        product = form.cleaned_data["product"]
        images = self.request.FILES.getlist("image")
        for image in images:
            ProductImages.objects.create(product=product, image=image)
        return super().form_valid(form)


class DeleteProductImages(ContentManagerRequiredMixin, DeleteView):
    model = ProductImages
    template_name = "pages/ecommerce/delete_product_image.html"
    success_url = reverse_lazy("ecommerce:list_product_images")


class ListProductView(ContentManagerRequiredMixin, ListView):
    """
    A view for listing all products.
    """

    model = Product
    template_name = "pages/ecommerce/product_list.html"
    paginate_by = 10


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
    template_name = "pages/ecommerce/add_product.html"
    success_url = reverse_lazy("ecommerce:list_product")


class DeleteProductView(ContentManagerRequiredMixin, DeleteView):
    """
    A view for deleting an existing product.
    """

    model = Product
    template_name = "pages/ecommerce/delete_product.html"
    success_url = reverse_lazy("ecommerce:list_product")


class ProductDetailView(ContentManagerRequiredMixin, ListView):
    """
    A view for listing all products.
    """

    model = Product
    template_name = "ecommerce/product_detail.html"


# --------------------------- Product views ends here -------


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
    paginate_by = 10


# ------------------------------- Tag views ends here


class AddReviewsView(LoginRequiredMixin, CreateView):
    model = ProductReview
    form_class = ProductReviewForm

    def form_valid(self, form):
        """
        Saves the form data and returns a JSON response containing the user's username,
        the review text, the rating,
        and the average rating for the product.

        Parameters:
            form (ProductReviewForm): The form containing the review data.

        Returns:
            JsonResponse: A JSON response containing the following keys:
                - bool (bool): True if the form is valid, False otherwise.
                - context (dict): A dictionary containing the user's username,
                  the review text, and the rating.
                - average_review (dict): A dictionary containing the average rating for
                the product.

        Raises:
            Product.DoesNotExist: If the product with the
            given primary key does not exist.
        """
        # Check if the user is authenticated and if the user has added a review already
        product = form.instance.product

        form.instance.user = self.request.user
        form.instance.product = Product.objects.get(pk=self.kwargs["pk"])
        self.object = form.save()

        average_review = ProductReview.objects.filter(product=product).aggregate(
            rating=Avg("rating"),
        )

        context = {
            "user": self.request.user.name,
            "review": form.instance.review,
            "rating": form.instance.rating,
        }

        return JsonResponse(
            {
                "bool": True,
                "context": context,
                "average_review": average_review,
            },
        )

    def form_invalid(self, form):
        return JsonResponse(
            {
                "bool": False,
                "errors": form.errors,
            },
        )
