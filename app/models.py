from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=155)
    price = models.FloatField()
    image = models.ImageField(upload_to='product/')

    def __str__(self):
        return self.title
