from django.db import models
from .customer import Customer
from .payment_type import PaymentType

class Order(models.Model):
 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")


    # def get_absolute_url(self):
    #     return reverse("Order_detail", kwargs={"pk": self.pk})
