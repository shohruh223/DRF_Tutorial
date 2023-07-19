from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=155)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
