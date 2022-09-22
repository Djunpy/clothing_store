from django import template

from products.models import Product, Category
from orders.models import Order

register = template.Library()


@register.inclusion_tag('inc/related_products.html')
def related_products():
    related = Product.objects.select_related('category').order_by('-id')[:3]
    return {'related_products': related}


@register.inclusion_tag('inc/category.html')
def show_category():
    categories = Category.objects.all()
    return {'categories': categories}


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.select_related('customer').filter(customer=user, ordered=False)
        if qs.exists():
            return qs[0].products.count()
    return 0
