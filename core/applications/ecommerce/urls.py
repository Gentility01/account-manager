from django.urls import path

from core.applications.ecommerce import views

app_name = "ecommerce"
urlpatterns = [
    path("add-product", views.AddProductView.as_view(), name="add_product"),
    path("add-category", views.AddCategoryView.as_view(), name="add_category"),
    path("list-category", views.ListCategoryView.as_view(), name="list_category"),
    path(
        "edit-category/<int:pk>/",
        views.EditCategoryView.as_view(),
        name="edit_category",
    ),
    path(
        "delete-category/<int:pk>/",
        views.DeleteCategoryView.as_view(),
        name="delete_category",
    ),
    path("list-product", views.ListProductView.as_view(), name="list_product"),
    path(
        "edit-product/<int:pk>/",
        views.EditProductView.as_view(),
        name="edit_product",
    ),
    path(
        "delete-product/<int:pk>/",
        views.DeleteProductView.as_view(),
        name="delete_product",
    ),
    path(
        "product-detail/<int:pk>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("add-tags", views.CreateProductTags.as_view(), name="add_tags"),
    path("list-tags", views.ListProductTags.as_view(), name="list_tags"),
    path("edit-tags/<int:pk>/", views.EditProductTags.as_view(), name="edit_tags"),
    path(
        "delete-tags/<int:pk>/",
        views.DeleteProductTags.as_view(),
        name="delete_tags",
    ),
    path(
        "create-product-image",
        views.ProductImagesCreateView.as_view(),
        name="create_product_image",
    ),
    path(
        "list-product-image",
        views.ListProductImages.as_view(),
        name="list_product_images",
    ),
    path(
        "update-product-image/<int:pk>/",
        views.UpdateProductImages.as_view(),
        name="update_product_image",
    ),
    path(
        "delete-product-image/<int:pk>/",
        views.DeleteProductImages.as_view(),
        name="delete_product_image",
    ),
    path(
        "product/<int:pk>/add-review/",
        views.AddReviewsView.as_view(),
        name="add_review",
    ),
    path("add-to-cart/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart", views.CartListView.as_view(), name="cart_list"),
    path(
        "delete-from-cart",
        views.DeleteFromCartView.as_view(),
        name="delete_from_cart_list",
    ),
]
