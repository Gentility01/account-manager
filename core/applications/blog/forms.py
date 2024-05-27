from ckeditor.widgets import CKEditorWidget
from django.forms import FileInput
from django.forms import ModelForm
from django.forms import NumberInput
from django.forms import Select
from django.forms import TextInput

from core.applications.blog.models import Banner
from core.applications.blog.models import BlogCategory
from core.applications.blog.models import Post


class BlogCategoryForm(ModelForm):
    class Meta:
        model = BlogCategory
        fields = [
            "title",
            "image",
            "sub_category",
        ]

        widgets = {
            "title": TextInput(
                attrs={"class": "form-control", "placeholder": "Enter  title"},
            ),
            "image": FileInput(attrs={"class": "form-control", "name": "filename"}),
            "sub_category": Select(attrs={"class": "form-control"}),
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "image",
            "content",
            "category",
            "tags",
        ]

        widgets = {
            "title": TextInput(
                attrs={"class": "form-control", "placeholder": "Enter post title"},
            ),
            "image": FileInput(attrs={"class": "form-control", "name": "filename"}),
            "content": CKEditorWidget(
                attrs={"class": "form-control", "placeholder": "Enter post content"},
            ),
            "category": Select(attrs={"class": "form-control"}),
            "tags": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter tags separate each by comma",
                },
            ),
        }


class BannerForm(ModelForm):
    class Meta:
        model = Banner
        fields = [
            "title",
            "sub_title",
            "image",
            "category",
            "price",
            "oldprice",
        ]

        widgets = {
            "title": TextInput(
                attrs={"class": "form-control", "placeholder": "Enter short title"},
            ),
            "sub_title": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter very short description",
                },
            ),
            "category": Select(attrs={"class": "form-control"}),
            "image": FileInput(attrs={"class": "form-control", "name": "filename"}),
            "price": NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter product price"},
            ),
            "oldprice": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product old price",
                },
            ),
        }
