import auto_prefetch
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import Permission
from django.db.models import CASCADE
from django.db.models import SET_NULL
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DecimalField
from django.db.models import IntegerField
from django.db.models import SlugField
from django.db.models import TextField
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from core.utils.choices import ProductStatus
from core.utils.choices import Rating
from core.utils.choices import Status
from core.utils.models import ImageTitleTimeBaseModels
from core.utils.models import TimeBasedModel
from core.utils.models import TitleandUIDTimeBasedModel
from core.utils.models import TitleTimeBasedModel

# Create your models here.


class Permissions:
    CAN_CRUD_PRODUCT = Permission.objects.filter(
        codename__in=["add_product", "change_product", "delete_product"],
    )
    CAN_CRUD_CATEGORY = Permission.objects.filter(
        codename__in=["add_category", "change_category", "delete_category"],
    )


class Tags(TitleTimeBasedModel): ...


class Category(ImageTitleTimeBaseModels):
    slug = SlugField(default="", blank=True)
    sub_category = auto_prefetch.ForeignKey(
        "self",
        on_delete=CASCADE,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        """
        Saves the instance with a slug generated from the title if no slug is provided.

        Parameters:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(TitleandUIDTimeBasedModel, ImageTitleTimeBaseModels):
    user = auto_prefetch.ForeignKey(
        "users.User",
        verbose_name=_("User"),
        on_delete=SET_NULL,
        null=True,
    )
    category = auto_prefetch.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=SET_NULL,
        null=True,
    )
    description = RichTextUploadingField("Description", default="", null=True)
    price = DecimalField(max_digits=100, decimal_places=2)
    oldprice = DecimalField(max_digits=100, decimal_places=2)
    spacification = RichTextUploadingField("specification", default="", null=True)

    product_status = CharField(
        choices=Status.choices,
        default=Status.IN_REVIEW,
        max_length=10,
    )
    tags = TaggableManager(blank=True, help_text="A comma-separated list of tags.")
    in_stock = BooleanField(default=True)
    featured = BooleanField(default=False)
    digital = BooleanField(default=True)
    best_seller = BooleanField(default=False)
    special_offer = BooleanField(default=False)
    just_arrived = BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Products"
        permissions = [
            ("can_crud_product", "Can create, update, and delete product"),
        ]

    def get_percentage(self, decimal_places=2):
        if self.oldprice > 0:
            percentage = ((self.oldprice - self.price) / self.oldprice) * 100
            return round(percentage, decimal_places)

        return 0

    # def get_discount_price

    def __str__(self):
        return self.title


class ProductImages(ImageTitleTimeBaseModels):
    product = auto_prefetch.ForeignKey(
        Product,
        verbose_name=_("Product image"),
        on_delete=SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name_plural = "Prouct images"


class CartOrder(TimeBasedModel):
    user = auto_prefetch.ForeignKey(
        "users.User",
        verbose_name=_("User Order"),
        on_delete=CASCADE,
        null=True,
    )
    price = DecimalField(max_digits=100, decimal_places=2)
    paid_status = BooleanField(default=False)
    product_status = CharField(
        choices=ProductStatus.choices,
        default=ProductStatus.PROCESSING,
        max_length=30,
    )

    class Meta:
        verbose_name_plural = "Cart Orders"


class CartOrderItems(TimeBasedModel):
    order = auto_prefetch.ForeignKey(
        CartOrder,
        verbose_name=_("Order"),
        on_delete=CASCADE,
        null=True,
    )
    item = CharField(max_length=200)
    image = CharField(max_length=200)
    quantity = IntegerField(default=0)
    price = DecimalField(max_digits=100, decimal_places=2)
    total = DecimalField(max_digits=100, decimal_places=2)
    invoice_no = CharField(max_length=20, default="", blank=True)

    class Meta:
        verbose_name_plural = "Cart Order Items"


class ProductReview(TimeBasedModel):
    user = auto_prefetch.ForeignKey(
        "users.User",
        verbose_name=_("User Review"),
        on_delete=SET_NULL,
        null=True,
    )
    product = auto_prefetch.ForeignKey(
        Product,
        verbose_name=_("Product Review"),
        on_delete=SET_NULL,
        null=True,
    )
    review = TextField()
    rating = IntegerField(choices=Rating.choices, default=Rating.THREE_STARS)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def get_rating(self):
        return self.rating


class WishList(TimeBasedModel):
    user = auto_prefetch.ForeignKey(
        "users.User",
        verbose_name=_("User Review"),
        on_delete=SET_NULL,
        null=True,
    )
    product = auto_prefetch.ForeignKey(
        Product,
        verbose_name=_("Product Wishlist"),
        on_delete=SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name_plural = "Wishlists"

    def get_rating(self):
        return f"products wishlist : {self.rating}"


class Address(TimeBasedModel):
    user = auto_prefetch.ForeignKey(
        "users.User",
        verbose_name=_("User Address"),
        on_delete=SET_NULL,
        null=True,
    )
    address = CharField(max_length=100, default="", blank=True)
    status = BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

    def get_rating(self):
        return f"products address : {self.address}"
