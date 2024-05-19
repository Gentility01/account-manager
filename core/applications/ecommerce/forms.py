from django.forms import CheckboxInput
from django.forms import FileInput
from django.forms import ModelForm
from django.forms import NumberInput
from django.forms import Select
from django.forms import Textarea
from django.forms import CharField
from django.forms import TextInput
from multiupload.fields import MultiFileField


from core.applications.ecommerce.models import Category
from core.applications.ecommerce.models import Product
from core.applications.ecommerce.models import Tags
from core.applications.ecommerce.models import ProductImages
from ckeditor.widgets import CKEditorWidget
from taggit.forms import TagField


class ProductForm(ModelForm):
    description = CharField(label='Description',
                   widget=Textarea(attrs={'class': 'ckeditor'}))
    tags = TagField(required=False)
    class Meta:
        model = Product
        fields = [
            "title",
            "image",
            "description",
            "price",
            "oldprice",
            "spacification",
            "tags",
            "product_status",
            "category",
            "in_stock",
            "featured",
            "digital",
            "best_seller",
            "special_offer",
            "just_arrived",

        ]
        widgets = {
            "title": TextInput(
                attrs={"class": "form-control", "placeholder": "Enter product name"},
            ),
            "image": FileInput(
                attrs={"class": "form-control", "id": "myFile", "name": "filename"},
            ),
            "description": CKEditorWidget(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product description",
                },
            ),
            "price": NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter product price"},
            ),
            "oldprice": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product old price",
                },
            ),
            "spacification": CKEditorWidget(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product spacification",
                },
            ),
            "tags": TextInput(attrs={"class": "form-control"}),
            "product_status": Select(
                attrs={"class": "form-control", "placeholder": "Enter product status"},
            ),
            "category": Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product category",
                },
            ),
            "in_stock": CheckboxInput(),
            "featured": CheckboxInput(),
            "digital": CheckboxInput(),
            "best_seller": CheckboxInput(),
            "special_offer": CheckboxInput(),
            "just_arrived": CheckboxInput(),
        }

class ProductImagesForm(ModelForm):
    """ Form to get all product images """
    image = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)

    class Meta:
        model = ProductImages
        fields = ["image", "product"]

        widgets = {
            "product": Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product",
                },
            ),
        }


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["title", "image", "sub_category"]
        widgets = {
            "title": TextInput(
                attrs={"class": "flex-grow", "placeholder": "Enter category name"},
            ),
            "image": FileInput(attrs={"class": "form-control", "name": "filename"}),
            "sub_category": Select(attrs={"class": "form-control"}),
        }


class TagsForm(ModelForm):
    class Meta:
        model = Tags
        fields = ["title"]
        widgets = {
            "title": TextInput(
                attrs={"class": "flex-grow", "placeholder": "Enter tag name"},
            ),
        }
