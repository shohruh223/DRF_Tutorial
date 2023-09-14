from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, integer_validator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=155)

    def __str__(self):
        return self.title


class Course(models.Model):
    video = models.FileField(upload_to="course/")
    title = models.CharField(max_length=155)
    user = models.ManyToManyField(to="app.User",
                                  related_name="courses")
    rating = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5)])
    comment = models.ForeignKey(to="app.User",
                                on_delete=models.CASCADE,
                                related_name="courses_comment")
    price = models.FloatField()
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(to="app.User",
                             on_delete=models.CASCADE,
                             related_name="comments")

    def __str__(self):
        return self.user


class Blog(models.Model):
    title = models.CharField(max_length=155)
    image = models.ImageField(upload_to="blog/")
    text = models.TextField()
    user = models.ForeignKey(to="app.User",
                             on_delete=models.CASCADE,
                             related_name="blogs")
    category = models.ForeignKey(to="app.Category",
                                 on_delete=models.CASCADE,
                                 related_name="blogs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Contact(models.Model):
    message = models.TextField()
    user = models.ForeignKey(to="app.User",
                             on_delete=models.CASCADE,
                             related_query_name="contacts")

    def __str__(self):
        return self.message


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have a phone number!')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6)
    activation_key_expires = models.DateTimeField(blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    serficate = models.FileField(upload_to="serficate/", null=True, blank=True)
    phone_number = models.CharField(max_length=25,
                                    validators=[integer_validator],
                                    unique=True, null=True, blank=True)
    experience = models.PositiveIntegerField(default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def save(self, *args, **kwargs):
        # Aktivatsiya muddatini offset-naive qilamiz
        if self.activation_key_expires:
            self.activation_key_expires = timezone.make_naive(self.activation_key_expires)

        super().save(*args, **kwargs)
