# import Paginator as Paginator

from loginAndRegister.models import Company, Category, Product, Users, PurchaseOrder, OderDetail
from adminFunctions.serializers import CompanySerializer, CategorySerializer, ProductSerializer, \
    PurchaseOrderSerializer, OderDetailSerializer
from loginAndRegister.serializers import UsersSerializer
from pewbill.responses import Response, SUCCESS_STATUS_CODE, ERROR_STATUS_CODE
from pewbill.responsesdescription import COMPANY_NOT_UPDATED, PRODUCT_NOT_UPDATED
from django.http import JsonResponse
from django.core.paginator import Paginator


def get_all_user_pagination(page, limit):
    try:
        user = Users.get_user()
        paginator = Paginator(user, limit)
        number_of_pages = paginator.num_pages
        total_users = paginator.count
        page_number = page
        user_final = paginator.get_page(page_number)
        user_serializer = UsersSerializer(user_final, many=True).data
        user_serializer.append({"total_pages": number_of_pages,
                                "total_users": total_users})

        return user_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


""" Company Action 
    so it providing company functions"""


def get_all_company():
    try:
        company = Company().get_company()
        company_serializer = CompanySerializer(company, many=True).data
        return company_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


def create_company_act(data):
    try:
        company = Company.create_company(data=data)
        company_serializer = CompanySerializer(company).data
        return Response.create_data(company_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def update_company(id=None, request=None):
    try:
        data = request.data
        data.update({"id": id})
        is_updated, company = Company.update_company(type=data)
        if is_updated:
            company_serializer = CompanySerializer(company).data
            return Response.create_data(company_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=COMPANY_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_company(id):
    try:
        company = Company.get_one_company(pk=id)
        company_serializer = CompanySerializer(company, many=False).data
        return JsonResponse(company_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_company(id):
    try:
        Company.delete_single_company(pk=id)
        return Response.create_success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))


""" Category Action 
    so it providing category functions"""


def get_all_category():
    try:
        category = Category().get_category()
        category_serializer = CategorySerializer(category, many=True).data
        return category_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


def create_category_act(data):
    try:
        category = Category.create_category(data=data)
        category_serializer = CategorySerializer(category).data
        return Response.create_data(category_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def update_category_act(id=None, request=None):
    try:
        data = request.data
        data.update({"id": id})
        is_updated, category = Category.update_category(type=data)
        if is_updated:
            category_serializer = CategorySerializer(category).data
            return Response.create_data(category_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=COMPANY_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_category(id):
    try:
        category = Category.get_one_category(pk=id)
        category_serializer = CategorySerializer(category, many=False).data
        return JsonResponse(category_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_category(id):
    try:
        Category.delete_single_category(pk=id)
        return Response.create_success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))


""" Product Action 
    so it providing product functions"""


def get_all_product():
    try:
        product = Product().get_product()
        product_serializer = ProductSerializer(product, many=True).data
        return product_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


def create_product_act(data):
    try:
        product = Product().create_product(data=data)
        product_serializer = ProductSerializer(product).data
        return Response.create_data(product_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def update_product_act(id=None, request=None):
    try:
        data = request.data
        data.update({"id": id})
        is_updated, product = Company.update_product(type=data)
        if is_updated:
            product_serializer = CompanySerializer(product).data
            return Response.create_data(product_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=PRODUCT_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_product(id):
    try:
        product = Product.get_one_product(pk=id)
        product_serializer = ProductSerializer(product, many=False).data
        return JsonResponse(product_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_product(id):
    try:
        Product.delete_single_product(pk=id)
        return Response.create_success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))


""" Purchase Order Action 
    so it providing purchase order functions"""


def get_all_purchase_order():
    try:
        purchase_order = PurchaseOrder().get_purchase_order()
        purchase_order_serializer = PurchaseOrderSerializer(purchase_order, many=True).data
        return purchase_order_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


def create_purchase_order_act(data):
    try:
        purchase_order = PurchaseOrder().create_purchase_order(data=data)
        purchase_order_serializer = PurchaseOrderSerializer(purchase_order).data
        return Response.create_data(purchase_order_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def update_purchase_order_act(id=None, request=None):
    try:
        data = request.data
        data.update({"id": id})
        is_updated, purchase_order = PurchaseOrder().update_purchase_order(type=data)
        if is_updated:
            purchase_order_serializer = PurchaseOrderSerializer(purchase_order).data
            return Response.create_data(purchase_order_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=PRODUCT_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_purchase_order(id):
    try:
        purchase_order = PurchaseOrder().get_one_purchase_order(pk=id)
        purchase_order_serializer = PurchaseOrderSerializer(purchase_order, many=False).data
        return JsonResponse(purchase_order_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_purchase_order(id):
    try:
        PurchaseOrder.delete_single_purchase_order(pk=id)
        return Response.create_success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))


""" Oder Detail Action 
    so it providing oder detail functions"""


def get_all_order_detail():
    try:
        order_detail = OderDetail().get_order_detail()
        order_detail_serializer = OderDetailSerializer(order_detail, many=True).data
        return order_detail_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


def create_order_detail_act(data):
    try:
        order_detail = OderDetail().create_order_detail(data=data)
        order_detail_serializer = OderDetailSerializer(order_detail).data
        return Response.create_data(order_detail_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def update_order_detail_act(id=None, request=None):
    try:
        data = request.data
        data.update({"id": id})
        is_updated, order_detail = OderDetail().update_order_detail(type=data)
        if is_updated:
            order_detail_serializer = OderDetailSerializer(order_detail).data
            return Response.create_data(order_detail_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=PRODUCT_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))

def get_single_order_detail(id):
    try:
        order_detail = OderDetail().get_one_order_detail(pk=id)
        order_detail_serializer = OderDetailSerializer(order_detail, many=False).data
        return JsonResponse(order_detail_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_order_detail(id):
    try:
        OderDetail().delete_single_order_detail(pk=id)
        return Response.create_success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))