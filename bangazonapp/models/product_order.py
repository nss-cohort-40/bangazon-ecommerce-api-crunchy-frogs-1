from django.db import models
from .order import Order
from .product import Product


class ProductOrder(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, )

    class Meta:
        verbose_name = ("ProductOrder")
        verbose_name_plural = ("ProductOrders")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ProductOrder_detail", kwargs={"pk": self.pk})

