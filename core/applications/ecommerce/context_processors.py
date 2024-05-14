from core.applications.ecommerce.models import Category
from core.applications.ecommerce.models import Product


def product_list(request):
    """
    Context processor to provide a list of products to templates.

    :param request: HTTP request object
    :return: Dictionary containing the product list
    """
    products = Product.objects.all()
    in_stock = products.filter(in_stock=True)

    best_seller = products.filter(best_seller=True)
    special_offer = products.filter(special_offer=True)
    featured = products.filter(featured=True)
    just_arrived = products.filter(just_arrived=True)
    just_arrived2 = products.filter(just_arrived=True).order_by("-id")
    categories = Category.objects.all().order_by("-id")

    return {
        "in_stock": in_stock,
        "best_seller": best_seller,
        "special_offer": special_offer,
        "featured": featured,
        "top_categories": categories,
        "just_arrived": just_arrived,
        "just_arrived2": just_arrived2,
        "all_products": products,
    }


def products_by_category(request):
    category_id = request.GET.get(
        "category_id",
    )  # Assuming the category_id is passed in the query parameters
    products = []
    if category_id:
        products = Product.objects.filter(category__id=category_id)
    return {"filtered_products": products}
