from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CartProduct, Product, Category, Discount
from orders.models import Order


class HomePageView(ListView):
    model = Product
    queryset = Product.objects.select_related('category').filter(available=True)[:8]
    template_name = 'home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discount'] = Discount.objects.all()[:2]
        context['categories'] = Category.objects.all()
        return context


class ProductsView(ListView):
    model = Product
    template_name = 'products.html'
    paginate_by = 6
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Весь ассортимент'
        return context

    def get_queryset(self):
        queryset = Product.objects.select_related('category').filter(available=True)
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # title
        return context

    def get_queryset(self):
        queryset = Product.objects.select_related('category').filter(available=True)
        return queryset


class ByCategoryView(ProductsView):
    # model = Product
    template_name = 'products.html'
    paginate_by = 2
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        queryset = Product.objects.select_related('category').filter(category__slug=self.kwargs['slug'], available=True)
        return queryset


class ByDiscountView(ProductsView):
    allow_empty = False
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Товары со скидкой'
        return context

    def get_queryset(self):
        queryset = Product.objects.select_related('category').filter(discount_id=self.kwargs['pk'], available=True)
        return queryset


class ByGenderView(ProductsView):
    paginate_by = 4
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = ''
        return context

    def get_queryset(self):

        queryset = Product.objects\
            .select_related('category')\
            .filter(Q(gender__iexact='men')
                    | Q(gender__iexact='women')
                    | Q(gender__iexact='children')
                    )
        return queryset


class AuthorizationPageView(View):
    def get(self, request):

        return render(self.request, 'auth.html')


class OrderSummaryView(LoginRequiredMixin, View):
    model = Order
    template_name = 'order-summary.html'

    def get(self, request, **kwargs):
        try:
            context = {
                'order': self.get_queryset()
            }
            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'У вас нет действующих заказов')
            return redirect('products')

    def get_queryset(self):
        queryset = Order.objects\
            .select_related('customer', 'coupon')\
            .get(customer=self.request.user, ordered=False)
        return queryset


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product, created = CartProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.products.filter(product_id=product.pk).exists():
            cart_product.quantity += 1
            cart_product.save()
            return redirect("/")
        else:
            order.products.add(cart_product)
            return redirect("/")
    else:
        order = Order.objects.create(customer=request.user)
        order.products.add(cart_product)
        return redirect("/")


@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            cart_product = CartProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            cart_product.delete()
            messages.info(request, f'Товар: {cart_product} удален из корзины')
            return redirect("order-summary")


# def remove_single_product_from_cart(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     order_qs = Order.objects.filter(
#         customer=request.user,
#         ordered=False
#     )
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.products.filter(product_id=product.pk).exists():
#             cart_product = CartProduct.objects.filter(
#                 product=product,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             if cart_product.quantity > 1:
#                 cart_product.quantity -= 1
#                 cart_product.save()
#             else:
#                 order.products.remove(cart_product)
#             return redirect("order-summary")
#         else:
#             return redirect("product-detail", product.get_absolute_url())
#     else:
#         return redirect("product-detail", product.get_absolute_url())
#


