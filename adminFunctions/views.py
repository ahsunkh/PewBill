from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from permissions import IsAdminUser
from pewbill.responses import Response
from pewbill.responsesdescription import INVALID_DATA
from utilities.pewbill_jwt import PewBillJWT
from adminFunctions.action import *


# get_all_company, create_company_act, update_company, get_single_company, delete_company, \
# get_all_category, create_category_act, get_single_category, delete_category, get_all_product, \
# create_product_act, update_category_act, update_company_act


class UserManagement(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                page = request.GET['page']
                limit = request.GET['limit']
                return Response.create_data(get_all_user_pagination(page=page, limit=limit))
        except Exception as err:
            return Response.error(str(err))


class CompanyGet(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_all_company())
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    # @content_type_validation
    def post(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return create_company_act(data=request.data)

            return Response.error(INVALID_DATA)
        except Exception as err:
            # raise
            return Response.error(str(err))


class CompanyDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    # @content_type_validation
    def put(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return update_company(id=pk, request=request)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def get(request, pk=None):

        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return get_single_company(id=pk)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    # @content_type_validation
    def delete(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return delete_company(id=pk)
        except Exception as err:
            return Response.error(str(err))


class TotalNumberCompanies(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_companies_stats())
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class CategoryGet(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_all_category())
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    # @content_type_validation
    def post(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return create_category_act(data=request.data)

            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class CategoryDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    # @content_type_validation
    def put(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return update_category_act(id=pk, request=request)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def get(request, pk=None):

        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return get_single_category(id=pk)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    # @content_type_validation
    def delete(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return delete_category(id=pk)
        except Exception as err:
            return Response.error(str(err))


class ProductGet(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_all_product())
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    # @content_type_validation
    def post(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return create_product_act(data=request.data)

            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class ProductDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    # @content_type_validation
    def put(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return update_product_act(id=pk, request=request)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def get(request, pk=None):

        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return get_single_product(id=pk)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    # @content_type_validation
    def delete(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return delete_product(id=pk)
        except Exception as err:
            return Response.error(str(err))


class PurchaseOrderGet(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_all_purchase_order())
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    # @content_type_validation
    def post(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return create_purchase_order_act(data=request.data)

            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class PurchaseOrderDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    # @content_type_validation
    def put(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return update_purchase_order_act(id=pk, request=request)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def get(request, pk=None):

        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return get_single_purchase_order(id=pk)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def delete(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return delete_purchase_order(id=pk)
        except Exception as err:
            return Response.error(str(err))


class OderDetailGet(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_all_order_detail())
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    # @content_type_validation
    def post(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return create_order_detail_act(data=request.data)

            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class OrderDetailDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def put(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return update_order_detail_act(id=pk, request=request)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def get(request, pk=None):

        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return get_single_order_detail(id=pk)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def delete(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return delete_order_detail(id=pk)
        except Exception as err:
            return Response.error(str(err))


class GetPurchaseOrderByON(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request, pk):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_by_order_details_by_po(id=pk))
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class PewStats(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            start_date = request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_po_registration_stats(start_date, end_date))
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class ChallanGet(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_all_challan())
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def post(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return create_challan_act(data=request.data)

            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class ChallanStats(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            start_date = request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_challan_registration_stats(start_date, end_date))
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class ChallanDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def put(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return update_challan_act(id=pk, request=request)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def get(request, pk=None):

        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return get_single_challan(id=pk)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    # @staticmethod
    # def get(request, pk=None):
    #
    #     try:
    #         user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
    #         if user_id:
    #             return get_single_challan(id=pk)
    #         return Response.error(INVALID_DATA)
    #     except Exception as err:
    #         return Response.error(str(err))

    @staticmethod
    def delete(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return delete_challan(id=pk)
        except Exception as err:
            return Response.error(str(err))


class ChallanByCompany(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return get_single_challan_by_company(id=pk)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class DeliveryRecordGet(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_all_delivery())
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class BillGet(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            company = request.GET.get('company')
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_all_bill(company=company))
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def post(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return create_bill_act(data=request.data)

            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class BillDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def put(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return update_bill_act(id=pk, request=request)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def get(request, pk=None):

        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return get_single_bill(id=pk)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))

    @staticmethod
    def delete(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return delete_bill(id=pk)
        except Exception as err:
            return Response.error(str(err))


class BillStats(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            start_date = request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return Response.create_data(get_bill_registration_stats(start_date, end_date))
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class CheckQuantity(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        try:
            order_detail_id = request.GET.get('order_detail')
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return get_check_quantity(order_detail_id=order_detail_id)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))
