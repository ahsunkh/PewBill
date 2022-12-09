from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from loginAndRegister.action import user_signup_email, user_signin_email, verify_user_email_signin_otp, update_user, \
    delete_user, logout_user, retrieve_po_data, user_forget_password, user_verify_forgot_otp, update_forget_password
from pewbill.responses import Response
from pewbill.responsesdescription import INVALID_DATA
from utilities.pewbill_jwt import PewBillJWT


# Create your views here.

class UserSignupEmail(APIView):

    @staticmethod
    def post(request):
        try:
            if request.data:
                return user_signup_email(data=request.data)
        except Exception as err:
            return Response.error(str(err))


class SigninEmail(APIView):

    @staticmethod
    def post(request):
        try:
            if request.data:
                return user_signin_email(request.data)
            return Response.error("Invalid request error")
        except Exception as err:
            return Response.error(str(err))


class SigninEmailVerifyOTP(APIView):

    @staticmethod
    def post(request):
        try:
            if request.data:
                return verify_user_email_signin_otp(request.data)
            return Response.error("Invalid request error")
        except Exception as err:
            return Response.error(str(err))


class UserUpdateDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            print(request)
            if user_id:
                return update_user(id=pk, data=request.data)
            return Response.error(INVALID_DATA)
        except Exception as err:
            return Response.error(str(err))


class UserForgetPassword(APIView):

    @staticmethod
    def post(request):
        try:
            if request.data:
                return user_forget_password(request.data)
            return Response.error("Invalid request error")
        except Exception as err:
            return Response.error(str(err))


class VerifyForgetPassword(APIView):

    @staticmethod
    def post(request):
        try:
            if request.data:
                return user_verify_forgot_otp(request.data)
            return Response.error("Invalid request error")
        except Exception as err:
            return Response.error(str(err))


class UpdateForgetPassword(APIView):

    @staticmethod
    def post(request):
        try:
            if request.data:
                return update_forget_password(request.data)
            return Response.error("Invalid request error")
        except Exception as err:
            return Response.error(str(err))


class UserDelete(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request, pk=None):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return delete_user(id=pk)
        except Exception as err:
            return Response.error(str(err))


class UserLogOut(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return logout_user(user_id, token)
        except Exception as err:
            return Response.error(str(err))


class RetrievePurchaseOrderData(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            user_id, token = PewBillJWT().parse_token(request.headers['Authorization'])
            if user_id:
                return retrieve_po_data(request=request)
        except Exception as err:
            return Response.error(str(err))
