
from core.utils.models import UIDTimeBasedModel, TitleTimeBasedModel, ImageBaseModels, TimeBasedModel, TitleandUIDTimeBasedModel
from core.utils.choices import ProductStatus, Status, Rating
from django.db.models import CharField, CASCADE, SET_NULL, TextField, DecimalField, BooleanField, IntegerField
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import Permission
from django_resized import ResizedImageField
from core.utils.media import MediaHelper
# from django.utils.html import mark_safe
import auto_prefetch

# Create your models here.

class Permissions:
    CAN_CRUD_PRODUCT = Permission.objects.filter(
        codename__in=['add_product', 'change_product', 'delete_product']
    )
    CAN_CRUD_CATEGORY = Permission.objects.filter(
        codename__in=['add_category', 'change_category', 'delete_category']
    )

class Tags(TitleTimeBasedModel):
    ...

class Category(TitleTimeBasedModel):
    image = ResizedImageField(upload_to=MediaHelper.get_image_upload_path)
    sub_category = auto_prefetch.ForeignKey(
        "self", on_delete=CASCADE, blank=True, null=True, related_name='subcategories'
    )


    class Meta:
        verbose_name_plural = "Categories"

    # def category_img(self):
    #     return mark_safe("<img src='%s' width=50 height=50 />")

    def __str__(self):
        return self.title


class Product(TitleandUIDTimeBasedModel, ImageBaseModels):
    user = auto_prefetch.ForeignKey("users.User", verbose_name=_("User"), on_delete=SET_NULL, null=True)
    category = auto_prefetch.ForeignKey(Category, verbose_name=_("Category"), on_delete=SET_NULL, null=True)
    description = TextField(null=True, blank=True)
    price = DecimalField(max_digits=100, decimal_places=2)
    oldprice = DecimalField(max_digits=100, decimal_places=2)
    spacification = TextField(null=True, blank=True)
    tags = auto_prefetch.ForeignKey(Tags, verbose_name=_("Tag"), on_delete=SET_NULL, null=True)
    product_status = CharField(choices=Status.choices, default=Status.IN_REVIEW, max_length=10)
    in_stock = BooleanField(default=True)
    featured = BooleanField(default=False)
    digital = BooleanField(default=True)
    best_seller = BooleanField(default=False)
    special_offer = BooleanField(default=False)
    just_arrived = BooleanField(default=True)
    # sku = ShortUUIDField(unique=True, length=10, max_length=20, prefix="sku", alphabet="abcdefghijklmnopqrstuvwxyz0123456789")

    class Meta:
        verbose_name_plural = "Products"
        permissions = [
            ('can_crud_product', 'Can create, update, and delete product'),
        ]

    def get_percentage(self, decimal_places=2):
        if self.oldprice > 0:
            percentage = ((self.oldprice - self.price) / self.oldprice) * 100
            return round(percentage, decimal_places)
        else:
            return 0  

    
    def __str__(self):
        return self.title
    

class ProductImages(ImageBaseModels, TimeBasedModel):
    product = auto_prefetch.ForeignKey(Product, verbose_name=_("Product image"), on_delete=SET_NULL, null=True)

    
    class Meta:
        verbose_name_plural = "Prouct images"










class CartOrder(TimeBasedModel):
    user = auto_prefetch.ForeignKey("users.User", verbose_name=_("User Order"),  on_delete=CASCADE, null=True)
    price = DecimalField(max_digits=100, decimal_places=2)
    paid_status = BooleanField(default=False)
    product_status = CharField(choices=ProductStatus.choices, default=ProductStatus.PROCESSING, max_length=30)

    class Meta:
        verbose_name_plural = "Cart Orders"

class CartOrderItems(TimeBasedModel):
     order = auto_prefetch.ForeignKey(CartOrder, verbose_name=_("Order"),  on_delete=CASCADE, null=True)
     item = CharField(max_length=200)
     image = CharField(max_length=200)
     quantity = IntegerField(default=0)
     price = DecimalField(max_digits=100, decimal_places=2)
     total = DecimalField(max_digits=100, decimal_places=2)
     invoice_no = CharField(max_length=20, null=True, blank=True)

     class Meta:
        verbose_name_plural = "Cart Order Items"




class ProductReview(TimeBasedModel):
    user = auto_prefetch.ForeignKey("users.User", verbose_name=_("User Review"),  on_delete=SET_NULL, null=True)
    product = auto_prefetch.ForeignKey(Product, verbose_name=_("Product Review"),  on_delete=SET_NULL, null=True)
    review = TextField()
    rating = IntegerField(choices=Rating)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def get_rating(self):
        return self.rating



class WishList(TimeBasedModel):
    user = auto_prefetch.ForeignKey("users.User", verbose_name=_("User Review"),  on_delete=SET_NULL, null=True)
    product = auto_prefetch.ForeignKey(Product, verbose_name=_("Product Wishlist"),  on_delete=SET_NULL, null=True)


    class Meta:
        verbose_name_plural = "Wishlists"

    def get_rating(self):
        return f"products wishlist : {self.rating}"


class Address(TimeBasedModel):
     user = auto_prefetch.ForeignKey("users.User", verbose_name=_("User Address"),  on_delete=SET_NULL, null=True)
     address = CharField(max_length=100, null=True)
     status = BooleanField(default=False)

     class Meta:
        verbose_name_plural = "Address"

     def get_rating(self):
        return f"products address : {self.address}"