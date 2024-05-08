from core.applications.ecommerce.models import Product, Category
# from django.core.exceptions import ObjectDoesNotExist

def product_list(request):
    """
    Context processor to provide a list of products to templates.
    
    :param request: HTTP request object
    :return: Dictionary containing the product list
    """
    in_stock = Product.objects.filter(in_stock=True)
    newly_arrived = Product.objects.filter(newly_arrived=True)
    best_seller = Product.objects.filter(best_seller=True)
    special_offer = Product.objects.filter(special_offer=True)
    featured = Product.objects.filter(featured=True)
    categories = Category.objects.all()[:5]

    return {
        "in_stock": in_stock, "newly_arrived": newly_arrived,
        "best_seller": best_seller, "special_offer": special_offer,
        "featured":featured, "top_categories": categories
    }
