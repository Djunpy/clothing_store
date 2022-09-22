from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', cache_page(60 * 5)(views.HomePageView.as_view()), name='home-page'),
    path('authorization/', views.AuthorizationPageView.as_view(), name='authorization'),
    path('products/', cache_page(60 * 5)(views.ProductsView.as_view()), name='products'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('by-gender/', views.ByGenderView.as_view(), name='by-gender'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('by-category/<slug:slug>/', views.ByCategoryView.as_view(), name='by-category'),
    path('by-discount/<int:pk>/', cache_page(60 * 5)(views.ByDiscountView.as_view()), name='by-discount'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('<slug:slug>/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
]