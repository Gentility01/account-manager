from django.contrib import admin
from core.applications.ecommerce.models import (
    Address, WishList, ProductReview, 
    CartOrderItems, CartOrder, ProductImages, 
    Product, Category, Tags
)

# from core.utils.permissions import CAN_MANAGE_BANNERS, CAN_MANAGE_BLOGS, CAN_MANAGE_PRODUCTS
# from django.contrib.auth.models import Group


# Register your models here.


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class TagAdmin(admin.ModelAdmin):
    list_display = ["id"]
admin.site.register(Tags, TagAdmin)



class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ["user", "title", "price", "image","in_stock", "digital", "best_seller", "just_arrived", "featured", "special_offer"]
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "display_image"]

    def display_image(self, obj):
        return obj.image.url if obj.image else ''

    display_image.short_description = 'Image Preview'
admin.site.register(Category, CategoryAdmin)



class CartOrderAdmin(admin.ModelAdmin):
    list_display = ["user", "price", "paid_status", "product_status"]
admin.site.register(CartOrder, CartOrderAdmin)



class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "rating"]
admin.site.register(ProductReview, ProductReviewAdmin)\


class WishListAdmin(admin.ModelAdmin):
    list_display = ["user", "product"]
admin.site.register(WishList, WishListAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "status"]
admin.site.register(Address, AddressAdmin)


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", "item", "quantity", "price", "invoice_no"]
admin.site.register(CartOrderItems, CartOrderItemsAdmin)


