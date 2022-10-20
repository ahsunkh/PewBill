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
    def get_user():
        try:
            return Users.objects.filter(role=2)
        except:
            return None

    @staticmethod
    def check_email_user(email=None):
        if email is not None:
            return Users.objects.filter(email=email).exists()
        return None

    @staticmethod
    def build_user_name(first_name, last_name):
        username = (first_name.lower())[::] + '_' + (last_name.lower())[:1]
        counter = 1

        while Users.check_user_by_username(username=username):
            username = username + str(counter)
            counter = counter + 1
        return username

    @staticmethod
    def is_token_exists(token=None, user_id=None):
        user = Users.objects.get(id=user_id)
        if token in user.jwt_token:
            return True
        return False

    @staticmethod
    def create_email_user(data=None):
        try:
            if data is not None:
                return Users.objects.create(**data)
        except Exception as err:
            return False

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

    @staticmethod
    def get_user_by_id(id=None):
        if id is not None:
            return Users.objects.get(id=id)
        return False

    @staticmethod
    def check_user_by_username(username=None):
        return Users.objects.filter(user_name=username).exists()


class Company(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)
    logo = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=15, default='')
    email = models.EmailField(null=False, blank=False)

    @staticmethod
    def get_company():
        return Company.objects.all()

    @staticmethod
    def create_company(data):
        try:
            if data is not None:
                return Company.objects.create(**data)
        except:
            return Response.error("invalid request")

    @staticmethod
    def update_company(type=None):
        if type is not None:
            try:
                Company.objects.filter(id=type.get('id')).update(**type)
                company = Company.objects.get(id=type.get('id'))
                return True, company
            except Exception as err:
                return False, {}
        return False, {}

    @staticmethod
    def get_one_company(pk):
        company = Company.objects.get(pk=pk)
        return company

    @staticmethod
    def delete_single_company(pk):
        company = Company.objects.get(pk=pk)
        company.delete()


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)

    @staticmethod
    def get_category():
        return Category.objects.all()

    @staticmethod
    def create_category(data):
        try:
            if data is not None:
                return Category.objects.create(**data)
        except:
            return Response.error("invalid request")

    @staticmethod
    def update_category(type=None):
        if type is not None:
            try:
                Category.objects.filter(id=type.get('id')).update(**type)
                category = Category.objects.get(id=type.get('id'))
                return True, category
            except Exception as err:
                return False, {}
        return False, {}

    @staticmethod
    def get_one_category(pk):
        category = Category.objects.get(pk=pk)
        return category

    @staticmethod
    def delete_single_category(pk):
        category = Category.objects.get(pk=pk)
        category.delete()


class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    unit_price = models.CharField(max_length=100, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @staticmethod
    def get_product():
        return Product.objects.all()

    @staticmethod
    def create_product(data):
        try:
            if data is not None:
                return Product.objects.create(**data)
        except:
            return Response.error("invalid request")

    @staticmethod
    def update_product(type=None):
        if type is not None:
            try:
                Product.objects.filter(id=type.get('id')).update(**type)
                product = Product.objects.get(id=type.get('id'))
                return True, product
            except Exception as err:
                return False, {}
        return False, {}

    @staticmethod
    def get_one_product(pk):
        product = Product.objects.get(pk=pk)
        return product

    @staticmethod
    def delete_single_product(pk):
        product = Product.objects.get(pk=pk)
        product.delete()


class PurchaseOrder(models.Model):
    purchase_order_number = models.CharField(null=False, blank=False, max_length=100)
    purchase_order_date = models.CharField(null=False, blank=False, max_length=100)
    delivery_date = models.CharField(null=False, blank=False, max_length=100)
    quantity = models.IntegerField(default=0)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    total_amount = models.CharField(max_length=100, blank=True)

    @staticmethod
    def get_purchase_order():
        return PurchaseOrder.objects.all()

    @staticmethod
    def create_purchase_order(data):
        try:
            if data is not None:
                return PurchaseOrder.objects.create(**data)
        except:
            return Response.error("invalid request")

    @staticmethod
    def update_purchase_order(type=None):
        if type is not None:
            try:
                PurchaseOrder.objects.filter(id=type.get('id')).update(**type)
                purchase_order = PurchaseOrder.objects.get(id=type.get('id'))
                return True, purchase_order
            except Exception as err:
                return False, {}
        return False, {}

    @staticmethod
    def get_one_purchase_order(pk):
        purchase_order = PurchaseOrder.objects.get(pk=pk)
        return purchase_order

    @staticmethod
    def delete_single_purchase_order(pk):
        purchase_order = PurchaseOrder.objects.get(pk=pk)
        purchase_order.delete()


class OderDetail(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    quantity = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_order_detail():
        return OderDetail.objects.all()

    @staticmethod
    def create_order_detail(data):
        try:
            if data is not None:
                return OderDetail.objects.create(**data)
        except:
            return Response.error("invalid request")

    @staticmethod
    def update_order_detail(type=None):
        if type is not None:
            try:
                OderDetail.objects.filter(id=type.get('id')).update(**type)
                order_detail = OderDetail.objects.get(id=type.get('id'))
                return True, order_detail
            except Exception as err:
                return False, {}
        return False, {}

    @staticmethod
    def get_one_order_detail(pk):
        return OderDetail.objects.get(pk=pk)

    @staticmethod
    def delete_single_order_detail(pk):
        order_detail = OderDetail.objects.get(pk=pk)
        order_detail.delete()
