from django.contrib import admin

from core.applications.ecommerce.models import Address
from core.applications.ecommerce.models import CartOrder
from core.applications.ecommerce.models import CartOrderItems
from core.applications.ecommerce.models import Category
from core.applications.ecommerce.models import Product
from core.applications.ecommerce.models import ProductImages
from core.applications.ecommerce.models import ProductReview
from core.applications.ecommerce.models import Tags
from core.applications.ecommerce.models import WishList


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = [
        "user",
        "title",
        "price",
        "image",
        "in_stock",
        "digital",
        "best_seller",
        "just_arrived",
        "featured",
        "special_offer",
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "display_image"]

    @admin.display(
        description="Image Preview",
    )
    def display_image(self, obj):
        return obj.image.url if obj.image else ""


@admin.register(CartOrder)
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ["user", "price", "paid_status", "product_status"]


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "rating"]


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ["user", "product"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "status"]


@admin.register(CartOrderItems)
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", "item", "quantity", "price", "invoice_no"]
