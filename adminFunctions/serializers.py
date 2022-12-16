from rest_framework import serializers
from loginAndRegister.models import Company, Category, Product, PurchaseOrder, OrderDetail, Challan, Bill, \
    DeliveryRecord , Contact


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_code', 'name', 'unit_price', 'category']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        # fields = ['id', 'purchase_order_number', 'purchase_order_date', 'company']


class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    purchase_order = PurchaseOrderSerializer(read_only=True)

    class Meta:
        model = OrderDetail
        fields = "__all__"


class ChallanSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(read_only=True)

    class Meta:
        model = Challan
        fields = "__all__"


class BillSerializer(serializers.ModelSerializer):
    challan = ChallanSerializer(read_only=True, many=True)

    # purchase_order = PurchaseOrderSerializer(read_only=True)

    class Meta:
        model = Bill
        fields = '__all__'
        # fields = ['id', 'bill_date', 'quantity', 'total_amount', 'challan', 'company', 'created_at', 'updated_at']


class DeliveryRecordSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(read_only=True)

    class Meta:
        model = DeliveryRecord
        fields = "__all__"


class PoStatsSerializer(serializers.ModelSerializer):
    created_at__date = serializers.DateField(read_only=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['created_at__date', 'count']


class ChallanStatsSerializer(serializers.ModelSerializer):
    created_at__date = serializers.DateField(read_only=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Challan
        fields = ['created_at__date', 'count']


class BillStatsSerializer(serializers.ModelSerializer):
    created_at__date = serializers.DateField(read_only=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Bill
        fields = ['created_at__date', 'count']

class ContactSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Contact
        fields = ['name', 'email', 'company']