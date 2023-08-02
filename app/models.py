from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=155)
    image = models.ImageField(upload_to='product/%Y-%m-%d/')
    user = models.ForeignKey(to='auth.User',
                             on_delete=models.CASCADE,
                             related_name="products")

    def __str__(self):
        return self.title
