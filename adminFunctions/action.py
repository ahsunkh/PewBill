from loginAndRegister.models import Company, Category, Product
from adminFunctions.serializers import CompanySerializer, CategorySerializer, ProductSerializer
from pewbill.responses import Response, SUCCESS_STATUS_CODE, ERROR_STATUS_CODE
from pewbill.responsesdescription import COMPANY_NOT_UPDATED, PRODUCT_NOT_UPDATED
from django.http import JsonResponse

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
