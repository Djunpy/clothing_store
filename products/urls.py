from django.urls import path
from django.views.decorators.cache import cache_page


from .views import (
    HomePageView, AuthorizationPageView, ProductsView, OrderSummaryView,ProductDetailView,
    ByCategoryView, ByGenderView, remove_from_cart, add_to_cart, ByDiscountView
)

urlpatterns = [
    path('', cache_page(60 * 5)(HomePageView.as_view()), name='home-page'),
    path('authorization/', AuthorizationPageView.as_view(), name='authorization'),
    path('products/', cache_page(60 * 5)(ProductsView.as_view()), name='products'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('by-gender/', ByGenderView.as_view(), name='by-gender'),
    path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('by-category/<slug:slug>/', ByCategoryView.as_view(), name='by-category'),
    path('by-discount/<int:pk>/', cache_page(60 * 5)(ByDiscountView.as_view()), name='by-discount'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('<slug:slug>/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]