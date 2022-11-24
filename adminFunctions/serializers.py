from rest_framework import serializers
from loginAndRegister.models import Company, Category, Product, PurchaseOrder, OrderDetail, Challan, Bill


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
        fields = ['id', 'product_id', 'name', 'unit_price', 'category']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'purchase_order_number', 'purchase_order_date',
                  'quantity', 'company', 'total_amount']


class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderDetail
        fields = "__all__"


class ChallanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challan
        fields = "__all__"


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"
