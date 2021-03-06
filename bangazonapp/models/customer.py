from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    class Meta:
        verbose_name = ("Customer")
        verbose_name_plural = ("Customers")


    def get_absolute_url(self):
        return reverse("Customer_detail", kwargs={"pk": self.pk})