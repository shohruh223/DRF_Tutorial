from django.db import models
from django.utils.timezone import localtime


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_formatted_created_time(self):
        format_str = '%Y-%m-%d %H:%M:%S'
        return localtime(self.created_at).strftime(format_str)


class Category(models.Model):
    title = models.CharField(max_length=180)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'


class Product(BaseModel):
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
