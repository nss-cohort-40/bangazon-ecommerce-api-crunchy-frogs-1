from django.db import models
from .customer import Customer


class PaymentType(models.Model):

    merchant_name = models.CharField(max_length=25)
    account_number = models.CharField(max_length=25)
    expiration_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = ("PaymentType")
        verbose_name_plural = ("PaymentTypes")

    # def get_absolute_url(self):
    #     return reverse("PaymentType_detail", kwargs={"pk": self.pk})
