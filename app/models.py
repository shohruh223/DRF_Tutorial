from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    title = models.CharField(max_length=180)

    def __str__(self):
        return self.title


class Product(BaseModel):
    image = models.ImageField(upload_to='product/')
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(to='app.Category',
                                 on_delete=models.CASCADE,
                                 related_name='products')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product'
