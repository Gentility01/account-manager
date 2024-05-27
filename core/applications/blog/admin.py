from django.contrib import admin

from core.applications.blog.models import Banner
from core.applications.blog.models import BlogCategory
from core.applications.blog.models import Post

# Register your models here.


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("title",)
    search_fields = ("title",)
    date_hierarchy = "created_at"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "slug", "user", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("category", "user", "created_at")
    search_fields = ("title", "content")
    date_hierarchy = "created_at"


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "sub_title", "category", "price", "oldprice"]
