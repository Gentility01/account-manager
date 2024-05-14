from django.db.models import TextChoices


class ProductStatus(TextChoices):
    PROCESSING = ("PROCESSING", "PROCESSING")
    SHIPPED = ("SHIPPED", "SHIPPED")
    DELIVERD = ("DELIVERD", "DELIVERD")


class Status(TextChoices):
    DRAFT = ("DRAFT", "DRAFT")
    DISABLED = ("DISABLED", "DISABLED")
    IN_REVIEW = ("IN_REVIEW", "IN_REVIEW")
    REJECTED = ("REJECTED", "REJECTED")
    PUBLISHED = ("PUBLISHED", "PUBLISHED")


Rating = (
    (1, "⭐"),
    (2, "⭐⭐"),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐"),
)
