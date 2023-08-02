from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app.models import Product
from io import BytesIO


class ProductCRUDTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_image(self):
        # Rasm yaratish
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Rasmni serverga yuborish uchun SimpleUploadedFile obyektiga o'girish
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")

        # Rasm yaratilganligini va o'zgaruvchi sifatida qaytarilayotganligini tekshirish
        return image_file

    def test_create_product(self):
        # Foydalanuvchi obyektini yaratish
        user = User.objects.create(username="shox")

        # Test ma'lumotlarini tuzish
        data = {"title": "Test Title", "user": user.id}

        # Test rasm yaratish va dataga qo'shish
        data['image'] = self.test_create_image()

        # To'g'ri URL ni olish va "basename" qo'shish
        url = reverse('product-list')  # product-list URL for Product viewset

        # Test ma'lumotlarini serverga POST so'rov bilan yuborish
        response = self.client.post(path=url, data=data, format='multipart')

        # Javobni tekshirish
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

        # Product obyektini bazadan olamiz va ma'lumotlarini tekshirish
        product = Product.objects.get()
        self.assertEqual(product.title, "Test Title")
        self.assertIsNotNone(product.image)  # Rasm maydoni bo'sh bo'lmasligini tekshirish

    def test_retrieve_product(self):
        # Foydalanuvchi obyektini yaratish
        user = User.objects.create(username="shox")

        # Product obyektini yaratish
        product = Product.objects.create(title="Test Product", user=user)

        # To'g'ri URL ni olish va "basename" qo'shish
        url = reverse('product-detail', args=[product.id])  # product-detail URL for Product viewset

        # Product obyektini serverdan GET so'rov bilan o'qish
        response = self.client.get(path=url)

        # Javobni tekshirish
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], product.title)

    def test_update_product(self):
        # Foydalanuvchi obyektini yaratish
        user = User.objects.create(username="shox")

        # Product obyektini yaratish
        product = Product.objects.create(title="Test Product", user=user)

        # Test ma'lumotlarini tuzish
        data = {"title": "Updated Test Product", "user": user.id}

        # Test rasm yaratish va dataga qo'shish
        data['image'] = self.test_create_image()

        # To'g'ri URL ni olish va "basename" qo'shish
        url = reverse('product-detail', args=[product.id])  # product-detail URL for Product viewset

        # Test ma'lumotlarini serverga PUT so'rov bilan yuborish
        response = self.client.put(path=url, data=data, format='multipart')

        # Javobni tekshirish
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Product obyektini bazadan yangilab olish va ma'lumotlarini tekshirish
        product.refresh_from_db()
        self.assertEqual(product.title, data['title'])

    def test_delete_product(self):
        # Foydalanuvchi obyektini yaratish
        user = User.objects.create(username="shox")

        # Product obyektini yaratish
        product = Product.objects.create(title="Test Product", user=user)

        # To'g'ri URL ni olish va "basename" qo'shish
        url = reverse('product-detail', args=[product.id])  # product-detail URL for Product viewset

        # Obyektni o'chirish uchun serverga DELETE so'rovini yuborish
        response = self.client.delete(path=url)

        # Javobni tekshirish
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

        # Obyekt bazadan o'chirilganligini tekshirish
        with self.assertRaises(Product.DoesNotExist):
            product = Product.objects.get(id=product.id)




