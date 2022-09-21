from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Discount(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bulletin = models.BooleanField(default=False)
    percent = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    ends = models.DateTimeField(blank=True, null=True)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('by-discount', args=[self.pk])

    def __str__(self):
        return f'{self.name}, {self.percent}%'


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        return reverse('by-category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    CLOTHING_SIZE = (
        ('M', 44),
        ('L', 46),
        ('XL', 48)
    )

    GENDERS_CHOICE = (
        ('men', 'Men'),
        ('women', 'Women'),
        ('children', 'Children')
    )
    favorites = models.ManyToManyField(get_user_model(), blank=True)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique_for_date='created')
    size = models.CharField(
        choices=CLOTHING_SIZE,
        default=44, max_length=2
    )
    gender = models.CharField(
        choices=GENDERS_CHOICE, max_length=15,
        blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug, self.pk])

    def __str__(self):
        return self.name


class CartProduct(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_discount_sum(self):
        if self.product.discount.available is not False:
            return self.get_total_product_price() * self.product.discount.percent / 100
        return 0

    def get_total_discount_item_price(self):
        return self.get_total_product_price() - self.get_discount_sum()

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product.discount:
            return self.get_total_discount_item_price()
        return self.get_total_product_price()

    def __str__(self):
        return f'Cart: {self.pk}, by: {self.user.username}'