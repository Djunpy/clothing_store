from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_countries.fields import CountryField

from products.models import CartProduct


class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct)
    created = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        'Coupon',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    being_delivered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address',
        related_name='shipping_address',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    def get_total_cost(self):
        return sum(product.get_final_price() for product in self.products.all())

    def get_final_cost(self):
        if self.coupon:
            return self.get_total_cost() * self.coupon.percent / 100
        return self.get_total_cost()

    def get_absolute_url(self):
        return reverse('cart', args=[self.pk])

    def __str__(self):
        return f'Order: {self.pk}, by: {self.customer.username}'


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    percent = models.FloatField()

    def __str__(self):
        return self.code


class Address(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    country = CountryField(multiple=False)
    street_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'