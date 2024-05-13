from core.applications.ecommerce.models import Product, Category
# from django.core.exceptions import ObjectDoesNotExist

def product_list(request):
    """
    Context processor to provide a list of products to templates.
    
    :param request: HTTP request object
    :return: Dictionary containing the product list
    """
    in_stock = Product.objects.filter(in_stock=True)
    best_seller = Product.objects.filter(best_seller=True)
    special_offer = Product.objects.filter(special_offer=True)
    featured = Product.objects.filter(featured=True)
    just_arrived = Product.objects.filter(just_arrived=True)
    just_arrived2 = Product.objects.filter(just_arrived=True).order_by("-id")
    categories = Category.objects.all().order_by("-id")
    all_products = Product.objects.all()
    return {
        "in_stock": in_stock,
        "best_seller": best_seller, "special_offer": special_offer,
        "featured":featured, "top_categories": categories,
        "just_arrived":just_arrived, "just_arrived2":just_arrived2,
        "all_products":all_products
    }



def products_by_category(request):
    category_id = request.GET.get('category_id')  # Assuming the category_id is passed in the query parameters
    products = []
    if category_id:
        products = Product.objects.filter(category__id=category_id)
    return {'filtered_products': products}