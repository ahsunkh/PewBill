import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Count

from pewbill.responses import Response


# Create your models here.

class Roles(models.Model):
    role = models.CharField(max_length=50)
    details = models.TextField()

    class Meta:
        db_table = "Roles"

    @staticmethod
    def get_role_by_id(id=None):
        return Roles.objects.get(id=id)


class Users(models.Model):
    phone_number = models.CharField(max_length=15, default='')
    user_name = models.CharField(max_length=50)
    password = models.TextField(null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    customer_id = models.CharField(max_length=50, default='')
    jwt_token = ArrayField(
        models.TextField(), size=None, default=list)
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(blank=False, default=True)
    two_factor_auth = models.BooleanField(blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "Users"

    @staticmethod
    def get_user():
        try:
            return Users.objects.filter(role=2)
        except:
            return False

    @staticmethod
    def check_email_user(email=None):
        if email is not None:
            return Users.objects.filter(email=email).exists()
        return False

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
        return Users.objects.create(**data)

    @staticmethod
    def get_user_by_email(email=None):
        if email is not None:
            return Users.objects.get(email=email)
        return False

    @staticmethod
    def update_model_user(id=None, update_data=None):
        if update_data is not None:
            try:
                Users.objects.filter(id=id).update(**update_data)
                user = Users.objects.get(id=id)
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
    payment_terms = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "Company"

    @staticmethod
    def get_company():
        return Company.objects.all()

    @staticmethod
    def create_company(data):
        return Company.objects.create(**data)

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
        return Company.objects.get(id=pk)

    @staticmethod
    def delete_single_company(pk):
        company = Company.objects.get(id=pk)
        company.delete()


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = "Category"

    @staticmethod
    def get_category():
        return Category.objects.all()

    @staticmethod
    def create_category(data):
        return Category.objects.create(**data)

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
        return Category.objects.get(id=pk)

    @staticmethod
    def delete_single_category(pk):
        category = Category.objects.get(id=pk)
        category.delete()


class Product(models.Model):
    product_code = models.CharField(max_length=50, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    unit_price = models.FloatField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "Product"

    @staticmethod
    def get_product():
        return Product.objects.all()

    @staticmethod
    def create_product(data):
        return Product.objects.create(**data)

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
        return Product.objects.get(id=pk)

    @staticmethod
    def delete_single_product(pk):
        product = Product.objects.get(id=pk)
        product.delete()


class PurchaseOrder(models.Model):
    purchase_order_number = models.CharField(null=False, blank=False, max_length=100)
    purchase_order_date = models.CharField(null=False, blank=False, max_length=100)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "PurchaseOrder"

    @staticmethod
    def get_purchase_order(company_id):
        return PurchaseOrder.objects.filter(company_id=company_id)

    def get_total_po_registration(start_date, end_date):
        return PurchaseOrder.objects.values(
            'created_at__date').annotate(
            count=Count('id')).filter(
            created_at__date__range=[start_date, end_date]).order_by('created_at__date')

    @staticmethod
    def create_purchase_order(data):
        try:
            if data is not None:
                return PurchaseOrder.objects.create(**data)
        except Exception as err:
            print(err)
            return {}

    @staticmethod
    def update_purchase_order(id=None, update_data=None):
        print(update_data,222222222222222)
        if update_data is not None:
            try:
                purchase_order = PurchaseOrder.objects.filter(id=id).update(**update_data)
                return True, purchase_order
            except Exception as err:
                print(err)
                return False, {}
        return False, {}

    @staticmethod
    def get_one_purchase_order(pk):
        return PurchaseOrder.objects.get(id=pk)

    @staticmethod
    def delete_single_purchase_order(pk):
        purchase_order = PurchaseOrder.objects.get(id=pk)
        purchase_order.delete()


class OrderDetail(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    delivery_date = models.CharField(blank=True, max_length=100)
    quantity = models.IntegerField(blank=True)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "OrderDetail"

    @staticmethod
    def get_order_details_by_po_no(pk):
        order_details = OrderDetail.objects.filter(purchase_order=pk)
        return order_details

    @staticmethod
    def get_order_detail(po_id):
        return OrderDetail.objects.filter(purchase_order=po_id)

    @staticmethod
    def create_order_detail(data):
        return OrderDetail.objects.create(**data)

    @staticmethod
    def create_bulk_order_detail(data):
        return OrderDetail.objects.bulk_create(OrderDetail(**value) for value in data)

    @staticmethod
    def update_order_detail(id=None, data_order_detail=None):
        if data_order_detail is not None:
            try:
                order_detail = OrderDetail.objects.filter(id=id).update(**data_order_detail)
                return True, order_detail
            except Exception as err:
                print(err)
                return False, {}
        return False, {}

    @staticmethod
    def get_filter_purchase(pk):
        return OrderDetail.objects.filter(purchase_order=pk)

    @staticmethod
    def get_one_order_detail(pk):
        return OrderDetail.objects.get(id=pk)

    @staticmethod
    def check_order_detail_by_id(id):
        return OrderDetail.objects.filter(id=id).exists()

    @staticmethod
    def delete_single_order_detail(pk):
        order_detail = OrderDetail.objects.get(id=pk)
        order_detail.delete()


class Challan(models.Model):
    challan_date = models.CharField(null=False, blank=False, max_length=100)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.SET_NULL, null=True)
    bill = models.ForeignKey('Bill', on_delete=models.SET_NULL, null=True, related_name='challan')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "Challan"

    @staticmethod
    def get_challan(company_id):
        return Challan.objects.filter(order_detail__purchase_order__company_id=company_id)

    def get_total_challan_registration(start_date, end_date):
        return Challan.objects.values(
            'created_at__date').annotate(
            count=Count('id')).filter(
            created_at__date__range=[start_date, end_date]).order_by('created_at__date')

    @staticmethod
    def create_challan(data):
        return Challan.objects.create(**data)

    @staticmethod
    def update_challan(id=None, data=None):
        if data is not None:
            try:
                challan = Challan.objects.filter(id=id).update(**data)
                return True, challan
            except Exception as err:
                return False, {}
        return False, {}

    @staticmethod
    def update_challan_for_bill(id=None, data=None):
        if type is not None:
            try:
                challan = Challan.objects.filter(id=id).update(**data)
                # challan = Challan.objects.get(id=data.get('id'))
                return True, challan
            except Exception as err:
                return False, {}
        return False, {}

    @staticmethod
    def get_one_challan(pk):
        return Challan.objects.get(id=pk)

    @staticmethod
    def get_all_challan_by_order_id(pk):
        return Challan.objects.filter(order_detail=pk)

    @staticmethod
    def get_one_challan_by_company(pk):
        return Challan.objects.filter(order_detail__purchase_order__company_id=pk)

    @staticmethod
    def delete_single_challan(pk):
        challan = Challan.objects.get(id=pk)
        challan.delete()


class Bill(models.Model):
    bill_date = models.CharField(null=False, blank=False, max_length=100)
    quantity = models.IntegerField(blank=True)
    total_amount = models.DecimalField(max_digits=30, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "Bill"

    @staticmethod
    def get_bill(company):
        return Bill.objects.filter(company=company).prefetch_related('challan')

    @staticmethod
    def get_bill_with_challan():
        return Bill.objects.filter.prefetch_related('challan').all()

    @staticmethod
    def get_total_bill_registration(start_date, end_date):
        return Bill.objects.values(
            'created_at__date').annotate(
            count=Count('id')).filter(
            created_at__date__range=[start_date, end_date]).order_by('created_at__date')

    @staticmethod
    def create_bill(data):
        return Bill.objects.create(**data)

    @staticmethod
    def update_bill(type=None):
        if type is not None:
            try:
                Bill.objects.filter(id=type.get('id')).update(**type)
                bill = Bill.objects.get(id=type.get('id'))
                return True, bill
            except Exception as err:
                return False, {}
        return False, {}

    @staticmethod
    def get_one_bill(pk):
        return Bill.objects.prefetch_related('challan').get(id=pk)

    @staticmethod
    def delete_single_bill(pk):
        bill = Bill.objects.get(id=pk)
        bill.delete()


class DeliveryRecord(models.Model):
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.SET_NULL, null=True)
    quantity_delivered = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "DeliveryRecord"

    @staticmethod
    def get_delivery_record():
        return DeliveryRecord.objects.all()

    @staticmethod
    def create_delivery_record(data):
        return DeliveryRecord.objects.create(**data)

class Contact(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(null=False, unique=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "Contact"

    @staticmethod
    def get_all_contact(company_id):
        return Contact.objects.filter(company_id=company_id)

    @staticmethod
    def create_contact(data):
        return Contact.objects.create(**data)


