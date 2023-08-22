from django.urls import path
from app.views import ProductListView, ProductCreateView, ProductEditView, ProductDeleteView, ProductGetView


urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('add-product/', ProductCreateView.as_view(), name='add-product'),
    path('edit-product/<int:product_id>', ProductEditView.as_view(), name='edit-product'),
    path('product/<int:product_id>', ProductGetView.as_view(), name='product'),
    path('delete-product/<int:product_id>', ProductDeleteView.as_view(), name='delete-product'),

]