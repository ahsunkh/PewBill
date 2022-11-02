import json
import requests
from werkzeug.security import generate_password_hash, check_password_hash

from loginAndRegister.models import Roles, Users
from loginAndRegister.serializers import UsersSerializer

from pewbill.responses import Response, ERROR_STATUS_CODE_CONFLICT, ERROR_STATUS_CODE_FORBIDDEN, SUCCESS_STATUS_CODE, \
    ERROR_STATUS_CODE, ERROR_STATUS_CODE_NOT_FOUND
from pewbill.responsesdescription import USER_ALREADY_EXISTS, USER_DOES_NOT_CREATED, INVALID_EMAIL_ADDRESS, \
    USER_DOES_NOT_EXIST, OTP_SENT_ON_EMAIl, TRY_AGAIN, USER_NOT_UPDATED, LOG_OUT_SUCCESSFULLY, TOKEN_NOT_VALID
from pewbill.settings import OCR_SPACE_API_KEY
from scripts.sendEmail import SendEmail
from template.o_template import PewBillTemplate
from utilities.otp import PewBillOTP
from utilities.pewbill_jwt import PewBillJWT


def build_user_name(first_name, last_name):
    username = (first_name.lower())[::] + '_' + (last_name.lower())[:1]
    counter = 1

    while Users.check_user_by_username(username=username):
        username = username + str(counter)
        counter = counter + 1
    return username


def user_signup_email(data):
    try:
        if Users.check_email_user(email=data.get("email")):
            return Response.error(error_response=USER_ALREADY_EXISTS, status=ERROR_STATUS_CODE_CONFLICT)
        password = generate_password_hash(data.get('password'))
        data["password"] = password
        user_name = build_user_name(first_name=data['first_name'], last_name=data['last_name'])
        data.update({"user_name": user_name})
        users = Users.create_email_user(data=data)
        if users:
            return Response.success("user created")
        return Response.error(error_response=USER_DOES_NOT_CREATED, status=ERROR_STATUS_CODE_FORBIDDEN)

    except Exception as err:
        return Response.internal_server_error(str(err))


def user_signin_email(data):
    try:
        email = data.get("email", None)
        if Users.check_email_user(email=email):
            users = Users.get_user_by_email(email=email)
            tfa = users.two_factor_auth
            hash = users.password
            if check_password_hash(pwhash=hash, password=data['password']):
                if tfa:
                    send_otp = PewBillOTP().create_otp(data['email'])
                    content = PewBillTemplate().otp_mail_template_func(otp=send_otp)
                    subject = "Welcome to Email User Signin"
                    if SendEmail.send_email(reciever=email, subject=subject, content=content, name="PewBill"):
                        return Response.success(OTP_SENT_ON_EMAIl)
                    return Response.error(INVALID_EMAIL_ADDRESS)

                access, refresh = PewBillJWT().create_jwt(users)
                users_serializer = UsersSerializer(users).data
                users_serializer.update({"access_token": access,
                                         "refresh_token": str(refresh),
                                         })
                users.jwt_token.append(access)
                users.save()
                return Response.create_data(created_data_response=users_serializer, status=SUCCESS_STATUS_CODE)
            return Response.error("invalid password")
        return Response.error(USER_DOES_NOT_EXIST)
    except Exception as err:
        return Response.internal_server_error(str(err))


def verify_user_email_signin_otp(data):
    try:
        email_data = {"otp": data.get('otp'), "email": data.get('email')}
        if PewBillOTP().verify_otp_email(data=email_data):
            user = Users.get_user_by_email(email=data.get('email'))
            access, refresh = PewBillJWT().create_jwt(user)
            user_serializer = UsersSerializer(user).data
            user_serializer.update({"token": access,
                                    "refresh": str(refresh),
                                    "platform": "email"})
            user.jwt_token.append(access)
            user.save()
            return Response.create_data(created_data_response=user_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(TRY_AGAIN)
    except Exception as err:
        return Response.internal_server_error(str(err))


def update_user(id=None, data=None):
    try:

        if 'email' in data:
            return Response.error(error_response="You can not update your email",
                                  status=ERROR_STATUS_CODE)

        if 'password' in data:
            dict_a = {}
            password = generate_password_hash(data.get('password'))
            dict_a["password"] = password
            is_updated, user = Users.update_model_user(id=id, update_data=dict_a)
            if is_updated:
                user_serializer = UsersSerializer(user).data
                return Response.create_data(user_serializer, status=SUCCESS_STATUS_CODE)

        is_updated, user = Users.update_model_user(id=id, update_data=data)
        if is_updated:
            user_serializer = UsersSerializer(user).data
            return Response.create_data(user_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=USER_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def forget_password_action(data):
    try:
        user = Users.get_user_by_email(email=data.get('email'))
        password = generate_password_hash(data['password'])
        user.password = password
        user.save()
        user_serializer = UsersSerializer(user, many=False).data
        return user_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_user(id):
    try:
        Users.delete_single_user(pk=id)
        return Response.success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))


def logout_user(user_id=None, token=None):
    try:
        user = Users.get_user_by_id(id=user_id)
        if not user:
            return Response.error(error_response=USER_DOES_NOT_EXIST, status=ERROR_STATUS_CODE_NOT_FOUND)
        if token in user.jwt_token:
            user.jwt_token.remove(token)
            user.save()
            return Response.success(LOG_OUT_SUCCESSFULLY)
        return Response.error(TOKEN_NOT_VALID)
    except Exception as err:
        return Response.internal_server_error(str(err))


def add_roles_on_first_migrate():
    try:
        # Roles = getloop2.get_model('schema', 'Roles')
        default_roles_data = [{"id": 1, "role": "admin", "details": "an administration user"},
                              {"id": 2, "role": "user", "details": "a normal user"}]
        Roles.objects.bulk_create(Roles(**values) for values in default_roles_data)
        if (Roles.objects.all().count()) == len(default_roles_data):
            print("All roles successfully added")
            return
        print("Some roles may not created please check")
    except Exception as e:
        print("Roles not created", e)


def get_po_data_for_company_a(data):
    try:
        # po_number = data['ParsedResults'][0]['TextOverlay']['Lines'][4]['LineText']
        # purchase_order_date = data['ParsedResults'][0]['TextOverlay']['Lines'][6]['LineText']
        # delivery_date = data['ParsedResults'][0]['TextOverlay']['Lines'][29]['LineText']
        for i in data:
            print(i)
        # data = {"purchase_order_number": po_number[-7::],
        #         "purchase_order_date": purchase_order_date,
        #         "delivery_date":delivery_date,
        #         }
        # print(data)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_po_data_for_company_b(data):
    try:
        pass
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_po_data_for_company_c(data):
    try:
        print("CCCCCCCCCCCCCCCCCCCCCC")

    except Exception as err:
        return Response.internal_server_error(str(err))


def ocr_function(purchase_order_file):
    url = "https://api.ocr.space/parse/image"

    payload = {'language': 'eng',
               'isOverlayRequired': 'true',
               'detectOrientation': 'true',
               'isTable': 'true',
               'OCREngine': '5'}
    files = [
        ('file', ('po.png', purchase_order_file.read(), 'image/png'))
    ]
    headers = {
        'apikey': OCR_SPACE_API_KEY
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return json.loads(response.text)


def retrieve_po_data(request):
    try:
        company = (request.data.get('company'))
        purchase_order = (request.FILES.get('purchase_order'))

        json_purchase_order = ocr_function(purchase_order_file=purchase_order)

        if company == 'A':
            get_po_data_for_company_a(data=json_purchase_order)
        elif company == 'B':
            get_po_data_for_company_b(data=json_purchase_order)
        elif company == 'C':
            get_po_data_for_company_c(data=json_purchase_order)

    except Exception as err:
        return Response.internal_server_error(str(err))
