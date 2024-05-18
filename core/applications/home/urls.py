from django.urls import path

from core.applications.home import views

app_name = "homeapp"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("shop", views.ProductShopListView.as_view(), name="shop_list"),
    path("products/<slug:category_slug>/", views.ProductsCategoryList.as_view(), name="category_list"),
    path('product/<int:pk>/', views.ProductShopDetailView.as_view(), name='product_detail'),
]
