from django.urls import path
from app.views import add_product, product_list, get_product, edit_product, delete_product

urlpatterns = [
    path('add-product/', add_product, name='add-product'),
    path('product/', product_list, name='products'),
    path('product/<int:product_id>', get_product, name='product'),
    path('edit-product/<int:product_id>', edit_product, name='edit-product'),
    path('delete-product/<int:product_id>', delete_product, name='delete-product'),
]