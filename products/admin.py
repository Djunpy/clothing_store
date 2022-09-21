from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from .models import Product, CartProduct, Category, Discount
from .forms import ProductForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('get_image', 'name',  'category', 'get_discount', 'price', 'created', 'available')
    list_filter = ('category', 'price', 'available', 'created')
    search_fields = ('name', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('available',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    def get_discount(self, obj):
        if obj.discount:
            return obj.discount.percent
        return 0


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'get_final_price', 'ordered')
    list_filter = ('user', 'ordered')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'created', 'ends', 'available')
    list_filter = ('name', 'created', 'available')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}