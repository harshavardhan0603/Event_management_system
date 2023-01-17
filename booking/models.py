from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import User 
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus


# class Order(models.Model):
#     name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
#     amount = models.FloatField(_("Amount"), null=False, blank=False)
#     status = CharField(
#         _("Payment Status"),
#         default=PaymentStatus.PENDING,
#         max_length=254,
#         blank=False,
#         null=False,
#     )
#     provider_order_id = models.CharField(
#         _("Order ID"), max_length=40, null=False, blank=False
#     )
#     payment_id = models.CharField(
#         _("Payment ID"), max_length=36, null=False, blank=False
#     )
#     signature_id = models.CharField(
#         _("Signature ID"), max_length=128, null=False, blank=False
#     )

#     def __str__(self):
#         return f"{self.id}-{self.name}-{self.status}"
# Create your models here.

class venue(models.Model):
    venue_name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    charges = models.IntegerField()
    image = models.CharField(max_length=100)
    ratings = models.IntegerField(default=0)
    n_ratings = models.IntegerField(default=0)


class booking_data(models.Model):
    user =models.ForeignKey(User, on_delete = models.CASCADE)
    venue_name = models.CharField(max_length=100)
    EventType = models.CharField(max_length=100)
    date = models.DateField()
    breakfast = models.IntegerField()
    lunch = models.IntegerField()
    TeaSnacks = models.IntegerField()
    dinner = models.IntegerField()
    Nonveg = models.BooleanField(default=False)
    NoofGuest = models.IntegerField()
    Amount = models.IntegerField(default=0)
    Decoration = models.CharField(max_length=100)

class booking_review(models.Model):
    booking = models.ForeignKey(booking_data,  on_delete = models.CASCADE, unique=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.IntegerField( default=0)
    comment = models.CharField(max_length=200)






 
    






