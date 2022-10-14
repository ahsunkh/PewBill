import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

from pewbill.responses import Response


# Create your models here.

class Roles(models.Model):
    role = models.CharField(max_length=50)
    details = models.TextField()


class Users(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=50)
    phone_number = models.CharField(max_length=15, default='')
    user_name = models.CharField(max_length=50)
    password = models.TextField(null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    customer_id = models.CharField(max_length=50, default='')
    jwt_token = ArrayField(
        models.TextField(), size=None, default=list)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    status = models.BooleanField(blank=False, default=True)
    two_factor_auth = models.BooleanField(blank=False, default=False)

    @staticmethod
    def check_email_user(email=None):
        if email is not None:
            return Users.objects.filter(email=email).exists()
        return None

    @staticmethod
    def create_email_user(data=None):
        try:
            if data is not None:
                return Users.objects.create(**data)
            return None
        except Exception as err:
            return Response.internal_server_error(str(err))

    @staticmethod
    def get_user_by_email(email=None):
        if email is not None:
            return Users.objects.get(email=email)
        return False

    @staticmethod
    def update_model_user(type=None):
        if type is not None:
            try:
                Users.objects.filter(id=type.get('id')).update(**type)
                user = Users.objects.get(id=type.get('id'))
                return True, user
            except Exception as err:
                return False, {}
        return False, {}

    @staticmethod
    def delete_single_user(pk):
        user = Users.objects.get(id=pk)
        user.delete()


class Company(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)
    logo = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=15, default='')
    email = models.EmailField(null=False, blank=False)


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)


class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    unit_price = models.CharField(max_length=100, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
