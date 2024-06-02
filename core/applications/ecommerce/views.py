from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import View

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
from core.applications.ecommerce.models import WishList
from core.utils.views import ContentManagerRequiredMixin


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


# ---------------------------  ----------------------------------
# ---------------------- Product views ends here ----------------


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


# ---------------------------  ----------------------------------
# ---------------------- Tag views ends here ----------------


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


# ---------------------------  ----------------------------------
# ---------------------- Add reviews ends here ----------------


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        """
        Adds a product to the cart session data.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse: A JSON response containing the updated cart
            data and the total number of items in the cart.

        Description:
            This function is used to add a product to the cart session data.
            It takes the request object as a parameter,
            along with any additional arguments and keyword arguments.
            The function retrieves the product details from the request GET parameters
            and creates a dictionary representation of the product.
            It then checks if there is already a cart data object in the session.
            If there is, it updates the quantity of the product
            if it already exists in the cart, otherwise
            it adds the product to the cart data. Finally,
            it returns a JSON response containing the updated
            cart data and the total number of items in the cart.
        """

        cart_product = {
            str(request.GET.get("id")): {
                "title": request.GET.get("title"),
                "quantity": request.GET.get("qty"),
                "price": request.GET.get("price"),
                "image": request.GET.get("image"),
                "pid": request.GET.get("product_id"),
            },
        }

        if "cart_data_obj" in request.session:
            cart_data = request.session["cart_data_obj"]
            product_id = str(request.GET.get("id"))
            if product_id in cart_data:
                cart_data[product_id]["quantity"] = int(
                    cart_product[product_id]["quantity"],
                )
            else:
                cart_data.update(cart_product)
            request.session["cart_data_obj"] = cart_data
        else:
            request.session["cart_data_obj"] = cart_product

        return JsonResponse(
            {
                "data": request.session["cart_data_obj"],
                "totalcartitems": len(request.session["cart_data_obj"]),
            },
        )


# ---------------------------  ----------------------------------
# ---------------------- Add to cart  ends here ----------------


class CartListView(TemplateView):
    """
    A view that displays the cart items and calculates the total amount.

    This view retrieves the cart data from the session and calculates the total amount
    based on the quantity and price of each item in the cart. It then renders the
    'pages/ecommerce/cart_list.html' template, passing the cart data, total cart items,
    and total amount as context variables.
    """

    template_name = "pages/ecommerce/cart_list.html"

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and checks if the cart is empty.
        Redirects to the home page with a warning message if the cart is empty.
        """
        if (
            "cart_data_obj" not in request.session
            or not request.session["cart_data_obj"]
        ):
            messages.warning(request, "Your cart is empty.")
            return redirect("homeapp:home")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for the view.

        Parameters:
            **kwargs (dict): Additional keyword arguments.

        Returns:
            dict: The context data containing the following keys:
                - cart_data (dict): The cart data stored in the session.
                - totalcartitems (int): The total number of items in the cart.
                - cart_total_amount (float): The total amount of the items in the cart.
        """
        context = super().get_context_data(**kwargs)
        cart_total_amount = 0
        cart_data = self.request.session["cart_data_obj"]

        for product_id, item in cart_data.items():
            cart_total_amount += int(item["quantity"]) * float(item["price"])

        context["cart_data"] = cart_data
        context["totalcartitems"] = len(cart_data)
        context["cart_total_amount"] = cart_total_amount

        return context


# ---------------------------  ----------------------------------
# ---------------------- Cart List  ends here ----------------


class DeleteFromCartView(View):
    def get(self, request, *args, **kwargs):
        product_id = str(request.GET.get("id"))
        self.remove_item_from_cart(request, product_id)

        cart_total_amount = self.calculate_cart_total(request)

        context = render_to_string(
            "pages/async/cart_list.html",
            {
                "cart_data": request.session.get("cart_data_obj", {}),
                "totalcartitems": len(request.session.get("cart_data_obj", {})),
                "cart_total_amount": cart_total_amount,
            },
        )
        return JsonResponse(
            {
                "data": context,
                "totalcartitems": len(request.session.get("cart_data_obj", {})),
            },
        )

    def remove_item_from_cart(self, request, product_id):
        if "cart_data_obj" in request.session:
            cart_data = request.session["cart_data_obj"]
            if product_id in cart_data:
                del cart_data[product_id]
                request.session["cart_data_obj"] = cart_data

    def calculate_cart_total(self, request):
        cart_total_amount = 0
        if "cart_data_obj" in request.session:
            for item in request.session["cart_data_obj"].values():
                cart_total_amount += int(item["quantity"]) * float(item["price"])
        return cart_total_amount


# ---------------------------  ----------------------------------
# ---------------------- Delete from cart  ends here ----------------


class UpdateCartView(View):
    def get(self, request, *args, **kwargs):
        product_id = str(request.GET.get("id"))
        new_quantity = int(request.GET.get("quantity", 1))
        self.update_item_in_cart(request, product_id, new_quantity)

        cart_total_amount = self.calculate_cart_total(request)

        context = render_to_string(
            "pages/async/cart_list.html",
            {
                "cart_data": request.session.get("cart_data_obj", {}),
                "totalcartitems": len(request.session.get("cart_data_obj", {})),
                "cart_total_amount": cart_total_amount,
            },
        )
        return JsonResponse(
            {
                "data": context,
                "totalcartitems": len(request.session.get("cart_data_obj", {})),
            },
        )

    def update_item_in_cart(self, request, product_id, new_quantity):
        if "cart_data_obj" in request.session:
            cart_data = request.session["cart_data_obj"]
            if product_id in cart_data:
                cart_data[product_id]["quantity"] = new_quantity
                request.session["cart_data_obj"] = cart_data

    def calculate_cart_total(self, request):
        cart_total_amount = 0
        if "cart_data_obj" in request.session:
            for item in request.session["cart_data_obj"].values():
                cart_total_amount += int(item["quantity"]) * float(item["price"])
        return cart_total_amount


# ---------------------------  ----------------------------------
# ---------------------- Update Cart  ends here ----------------


class CheckoutView(TemplateView):
    template_name = "pages/ecommerce/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_total_amount = 0
        cart_data = self.request.session["cart_data_obj"]

        for product_id, item in cart_data.items():
            cart_total_amount += int(item["quantity"]) * float(item["price"])

        context["cart_data"] = cart_data
        context["totalcartitems"] = len(cart_data)
        context["cart_total_amount"] = cart_total_amount

        return context


class WishlistListView(LoginRequiredMixin, ListView):
    model = WishList
    template_name = "pages/ecommerce/wish_list.html"
    context_object_name = "wishlists"


def add_to_wishlist(request):
    product_id = request.GET.get("id")
    product = Product.objects.get(id=product_id)

    context = {}

    wishlist_count = WishList.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True,
        }
    else:
        new_wishlist = WishList.objects.create(
            product=product,
            user=request.user,
        )
        context = {
            "bool": True,
        }

    return JsonResponse(context)
