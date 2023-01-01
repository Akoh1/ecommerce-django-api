from django.db import models
from django.template.defaultfilters import slugify
import uuid
from django.core.files.storage import FileSystemStorage
from core.models.auth import User, BillingAddress
from typing import Union

fs = FileSystemStorage(location='../ecommerce/media/photos')


class Products(models.Model):
    prod_id = models.UUIDField(default=uuid.uuid4, editable=False)
    title: str = models.CharField(max_length=100)
    price: float = models.FloatField()
    stock: int = models.IntegerField()
    description: str = models.TextField(null=True, blank=True)
    # image = models.ImageField(storage=fs)
    image = models.ImageField(blank=True, null=True, upload_to="photos")
    slug = models.SlugField(default="-", unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        low_case = self.title.lower()
        grp_str = low_case.split(" ")
        res = "-".join(grp_str)
        slug = slugify(res + "-" + str(self.prod_id)[:7])
        self.slug = slug
        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    ordered: bool = models.BooleanField(default=False)
    num_of_prod: int = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.num_of_prod} of {self.product.title}"

    @property
    def total_price(self) -> float:
        return self.num_of_prod * self.product.price


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    bill_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL,
                                     blank=True, null=True)

    def __str__(self):
        return self.user.email

    @property
    def total_amount(self) -> float:
        total = 0
        for product_order in self.items.all():
            total += product_order.total_price
        return total
