from django.db import models


class Watch(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    price = models.PositiveIntegerField(blank=False, null=False, default=0)
    discount_base = models.PositiveIntegerField(blank=True, null=True)
    discount_amount = models.PositiveIntegerField(blank=True, null=True)
