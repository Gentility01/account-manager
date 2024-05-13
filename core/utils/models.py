from uuid import uuid4

import auto_prefetch
from django.db import models
from django.db.models.query import QuerySet
from model_utils import FieldTracker
from django_resized import ResizedImageField
from core.utils.media import MediaHelper


# def generate_uuid() -> str:
#     """
#     Generate a numeric UUID with 5 digits.
#     """
#     uuid = str(uuid4())
#     numeric_uuid = ''.join(filter(str.isdigit, uuid))
#     return numeric_uuid[:5]


class VisibleManager(auto_prefetch.Manager):
    def get_queryset(self) -> QuerySet:
        """filters queryset to return only visible items"""
        return super().get_queryset().filter(visible=True)


class TimeBasedModel(auto_prefetch.Model):
    # id = models.UUIDField(default=generate_uuid, editable=False, primary_key=True, serialize=False, unique=True)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True

    objects = auto_prefetch.Manager()
    items = VisibleManager()


class TitleTimeBasedModel(TimeBasedModel):
    title = models.CharField(max_length=50, null=True, blank=True)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True
        ordering = ["title", "created_at"]

    def __str__(self):
        return self.title


class TitleandUIDTimeBasedModel(TimeBasedModel):
    title = models.CharField(max_length=50, null=True, blank=True)
    # id = models.CharField(
    #     primary_key=True,
    #     default=generate_uuid,
    #     max_length=120,
    #     editable=False,
    #     unique=True,
    # )
    tracker = FieldTracker()

    class Meta(auto_prefetch.Model.Meta):
        abstract = True
        ordering = ["title","-created_at"]

    def __str__(self):
        return self.id


class UIDTimeBasedModel(TimeBasedModel):
    # id = models.CharField(
    #     primary_key=True,
    #     default=generate_uuid,
    #     max_length=120,
    #     editable=False,
    #     unique=True,
    # )
    tracker = FieldTracker()

    class Meta(auto_prefetch.Model.Meta):
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        return self.id


class BaseModel(UIDTimeBasedModel):
    created_by = auto_prefetch.ForeignKey("users.Account", on_delete=models.CASCADE, related_name="created_by")

    class Meta(auto_prefetch.Model.Meta):
        abstract = True

class ImageBaseModels(UIDTimeBasedModel):
    image = ResizedImageField(upload_to=MediaHelper.get_image_upload_path)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True
