import datetime
import os

import pdfkit

import templates.challan_template
from loginAndRegister.models import Company, Category, Product, Users, PurchaseOrder, OrderDetail, Challan, \
    Bill, DeliveryRecord, Contact
from adminFunctions.serializers import CompanySerializer, CategorySerializer, ProductSerializer, \
    PurchaseOrderSerializer, OrderDetailSerializer, BillSerializer, ChallanSerializer, \
    DeliveryRecordSerializer, PoStatsSerializer, ChallanStatsSerializer, BillStatsSerializer, ContactSerializer
from loginAndRegister.serializers import UsersSerializer
from pewbill.responses import Response, SUCCESS_STATUS_CODE, ERROR_STATUS_CODE
from pewbill.responsesdescription import COMPANY_NOT_UPDATED, PRODUCT_NOT_UPDATED, CHALLAN_NOT_UPDATED, \
    BILL_NOT_UPDATED, CATEGORY_NOT_UPDATED, \
    PURCHASE_ORDER_NOT_UPDATED, ORDER_DETAIL_NOT_UPDATED
from django.core.paginator import Paginator

from scripts.sendEmail import SendEmail


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
        return Response.create_data(company_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_company(id):
    try:
        Company.delete_single_company(pk=id)
        return Response.success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_companies_stats():
    try:
        company = Company().get_company()
        count = len(company)
        return {"total_number_of_companies": count}
    except Exception as err:
        return Response.internal_server_error(err)


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
        return Response.error(error_response=CATEGORY_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_category(id):
    try:
        category = Category.get_one_category(pk=id)
        category_serializer = CategorySerializer(category, many=False).data
        return Response.create_data(category_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_category(id):
    try:
        Category.delete_single_category(pk=id)
        return Response.success("item has been deleted")
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
        category_id = data.get("category")
        category_object = Category.get_one_category(pk=category_id)
        data['category'] = category_object

        product = Product().create_product(data=data)
        product_serializer = ProductSerializer(product).data
        return Response.create_data(product_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def update_product_act(id=None, request=None):
    try:
        data = request.data
        data.update({"id": id})
        is_updated, product = Product.update_product(type=data)
        if is_updated:
            product_serializer = ProductSerializer(product).data
            return Response.create_data(product_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=PRODUCT_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_product(id):
    try:
        product = Product.get_one_product(pk=id)
        product_serializer = ProductSerializer(product, many=False).data
        return Response.create_data(product_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_product(id):
    try:
        Product.delete_single_product(pk=id)
        return Response.success("Product deleted successfully.")
    except Exception as err:
        return Response.internal_server_error(str(err))


""" Purchase Order Action 
    so it providing purchase order functions"""


def get_all_purchase_order(company_id):
    try:
        purchase_order = PurchaseOrder().get_purchase_order(company_id=company_id)
        purchase_order_serializer = PurchaseOrderSerializer(purchase_order, many=True).data
        return purchase_order_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


def create_purchase_order_act(data):
    try:
        product_list = data.pop('product')
        quantity_list = data.pop('order_quantity')
        delivery_date = data.pop('delivery_date')

        company_obj = Company.get_one_company(pk=data.get('company'))
        data['company'] = company_obj
        purchase_order = PurchaseOrder().create_purchase_order(data=data)

        my_list = []
        for i in range(len(product_list)):
            product_obj = Product.get_one_product(pk=product_list[i])
            quantity = quantity_list[i]

            dict_order_detail = {"purchase_order": purchase_order,
                                 "product": product_obj,
                                 "quantity": quantity,
                                 "delivery_date": delivery_date}

            my_list.append(dict_order_detail)

        OrderDetail.create_bulk_order_detail(data=my_list)

        purchase_order_serializer = PurchaseOrderSerializer(purchase_order).data
        return Response.create_data(purchase_order_serializer)
    except Exception as err:

        return Response.internal_server_error(str(err))


def update_purchase_order_act(id=None, request=None):
    try:
        data = request.data
        data.update({"id": id})

        is_updated, purchase_order = PurchaseOrder().update_purchase_order(id=id, update_data=data)
        if is_updated:
            purchase_order_serializer = PurchaseOrderSerializer(purchase_order).data
            return Response.create_data(purchase_order_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=PURCHASE_ORDER_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_purchase_order(id):
    try:
        purchase_order = PurchaseOrder().get_one_purchase_order(pk=id)
        order_detail_filter = OrderDetail.get_filter_purchase(pk=id)
        for i in order_detail_filter:
            print(i.is_delivered == True)
            if i.is_delivered:
                purchase_order_status = True
                PurchaseOrder.update_purchase_order(id=id, update_data={"is_completed": purchase_order_status})
        purchase_order = PurchaseOrder().get_one_purchase_order(pk=id)
        purchase_order_serializer = PurchaseOrderSerializer(purchase_order, many=False).data
        return Response.create_data(purchase_order_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_purchase_order(id):
    try:
        PurchaseOrder.delete_single_purchase_order(pk=id)
        return Response.success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))


""" Oder Detail Action 
    so it providing oder detail functions"""


def get_all_order_detail(po_id):
    try:
        order_detail = OrderDetail().get_order_detail(po_id=po_id)
        order_detail_serializer = OrderDetailSerializer(order_detail, many=True).data
        return order_detail_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


def create_order_detail_act(data):
    try:
        order_detail = OrderDetail().create_order_detail(data=data)
        order_detail_serializer = OrderDetailSerializer(order_detail).data
        return Response.create_data(order_detail_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def update_order_detail_act(id=None, request=None):
    try:
        data = request.data
        data.update({"id": id})
        is_updated, order_detail = OrderDetail().update_order_detail(data_order_detail=data)
        if is_updated:
            order_detail_serializer = OrderDetailSerializer(order_detail).data
            return Response.create_data(order_detail_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=ORDER_DETAIL_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_order_detail(id):
    try:
        if OrderDetail().check_order_detail_by_id(id=id):
            order_detail = OrderDetail().get_one_order_detail(pk=id)
            order_total_quantity = order_detail.quantity
            list_challan = Challan.get_all_challan_by_order_id(pk=id)
            challan_total_quantity = 0

            for i in list_challan:
                challan_total_quantity = challan_total_quantity + i.quantity

            if order_total_quantity == challan_total_quantity:
                delivered = True
                OrderDetail.update_order_detail(id=id, data_order_detail={"is_delivered": delivered})
            order_detail = OrderDetail().get_one_order_detail(pk=id)
            order_detail_serializer = OrderDetailSerializer(order_detail, many=False).data
            return Response.create_data(order_detail_serializer)
        return Response.error("The provided order_id is invalid")
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_order_detail(id):
    try:
        OrderDetail().delete_single_order_detail(pk=id)
        return Response.success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_by_order_details_by_po(id):
    try:
        order_details = OrderDetail.get_order_details_by_po_no(pk=id)
        order_details_serializer = OrderDetailSerializer(order_details, many=True).data
        return order_details_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_po_registration_stats(start_date, end_date):
    try:
        list_dates = []
        list_counts = []

        if start_date == '' or end_date == '':
            start_date = (datetime.datetime.now() -
                          datetime.timedelta(days=15)).date()
            end_date = datetime.datetime.now().date()

        po_stats = PurchaseOrder.get_total_po_registration(
            start_date=start_date, end_date=end_date)
        po_stats_serializer = PoStatsSerializer(po_stats, many=True).data

        for item in po_stats_serializer:
            list_dates.append(item['created_at__date'])
            list_counts.append(item['count'])
        return {"dates": list_dates,
                "counts": list_counts}
    except Exception as err:
        return Response.internal_server_error(err)


""" Challan Action 
    so it providing challan functions"""


def get_all_challan(company_id):
    try:
        challan = Challan().get_challan(company_id=company_id)
        challan_serializer = ChallanSerializer(challan, many=True).data
        return challan_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_challan_registration_stats(start_date, end_date):
    try:
        list_dates = []
        list_counts = []

        if start_date == '' or end_date == '':
            start_date = (datetime.datetime.now() -
                          datetime.timedelta(days=15)).date()
            end_date = datetime.datetime.now().date()

        challan_stats = Challan.get_total_challan_registration(
            start_date=start_date, end_date=end_date)
        challan_stats_serializer = ChallanStatsSerializer(challan_stats, many=True).data

        for item in challan_stats_serializer:
            list_dates.append(item['created_at__date'])
            list_counts.append(item['count'])
        return {"dates": list_dates,
                "counts": list_counts}
    except Exception as err:
        return Response.internal_server_error(err)


def create_challan_act(data):
    try:
        if OrderDetail().check_order_detail_by_id(id=id):
            order_detail_obj = OrderDetail.get_one_order_detail(pk=data.get("order_detail"))
            data["order_detail"] = order_detail_obj
            challan = Challan().create_challan(data=data)
            dic_ = {"order_detail": order_detail_obj,
                    "quantity_delivered": data.get("quantity")}
            DeliveryRecord.create_delivery_record(dic_)

            product_name = challan.order_detail.product.name
            path_for_challan = '/home/affansidd/Desktop/PewBill/adminFunctions/challan/' + str(
                challan.order_detail.purchase_order.company.name) + '_' + 'challan' + '_' + str(challan.id) + '.pdf'
            content_for_pdf = templates.challan_template.challan_template_func(product_name=product_name)
            pdfkit.from_string(content_for_pdf, path_for_challan)

            challan_serializer = ChallanSerializer(challan).data
            return Response.create_data(challan_serializer)
        return Response.error("The provided order_id is invalid")
    except Exception as err:
        return Response.internal_server_error(str(err))


def update_challan_act(id=None, request=None):
    try:
        data = request.data
        data.update({"id": id})
        is_updated, challan = Challan().update_challan(id=id, data=data)
        if is_updated:
            challan_serializer = ChallanSerializer(challan).data
            return Response.create_data(challan_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=CHALLAN_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_challan(id):
    try:
        challan = Challan().get_one_challan(pk=id)
        challan_serializer = ChallanSerializer(challan, many=False).data
        return Response.create_data(challan_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_challan_send_by_email(id):
    try:
        challan = Challan().get_one_challan(pk=id)
        content = "Please find the attached challan"
        subject = "Challan"
        path_for_challan = '/home/affansidd/Desktop/PewBill/adminFunctions/challan/' + str(
            challan.order_detail.purchase_order.company.name) + '_' + 'challan' + '_' + str(challan.id) + '.pdf'
        name_file = str(challan.order_detail.purchase_order.company.name) + '_' + 'challan' + '_' + str(
            challan.id) + '.pdf'
        if SendEmail.send_email(reciever="m.affan@codexnow.com", attachment=True, name="PewBill", subject=subject,
                                content=content,
                                file_name=path_for_challan,
                                name_file=name_file):
            return Response.success("Challan successfully sent on email")
        return Response.error("Error on sending challan.")
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_challan_download(id):
    try:
        challan = Challan().get_one_challan(pk=id)

        product_name = challan.order_detail.product.name
        path_for_challan = '/home/affansidd/Desktop/PewBill/adminFunctions/challan/' + str(
            challan.order_detail.purchase_order.company.name) + '_' + 'challan' + '_' + str(challan.id) + '.pdf'
        content_for_pdf = templates.challan_template.challan_template_func(product_name=product_name)
        pdfkit.from_string(content_for_pdf, path_for_challan)

        return Response.success("File has been downloaded")
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_challan(id):
    try:
        Challan().delete_single_challan(pk=id)
        return Response.success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))


""" Delivery Action 
    so it providing delivery functions"""


def get_all_delivery():
    try:
        delivery_record = DeliveryRecord().get_delivery_record()
        delivery_record_serializer = DeliveryRecordSerializer(delivery_record, many=True).data
        return delivery_record_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))


""" Bill Action 
    so it providing Bill functions"""


def get_all_bill(company):
    try:
        bill = Bill().get_bill(company=company)

        bill_serializer = BillSerializer(bill, many=True).data
        return bill_serializer
    except Exception as err:
        print(err)
        return Response.internal_server_error(str(err))


def get_bill_registration_stats(start_date, end_date):
    try:
        list_dates = []
        list_counts = []

        if start_date == '' or end_date == '':
            start_date = (datetime.datetime.now() -
                          datetime.timedelta(days=15)).date()
            end_date = datetime.datetime.now().date()

        bill_stats = Bill.get_total_bill_registration(
            start_date=start_date, end_date=end_date)
        bill_stats_serializer = BillStatsSerializer(bill_stats, many=True).data

        for item in bill_stats_serializer:
            list_dates.append(item['created_at__date'])
            list_counts.append(item['count'])
        return {"dates": list_dates,
                "counts": list_counts}
    except Exception as err:
        return Response.internal_server_error(err)


def create_bill_act(data):
    try:

        challan_list = data.pop("challans")
        total_price = 0
        total_quantity = 0
        for i in challan_list:
            challan = Challan.get_one_challan(pk=i)
            quantity = challan.quantity
            total_quantity = total_quantity + quantity
            challan_serializer = ChallanSerializer(challan).data
            order_dict = dict(challan_serializer["order_detail"])
            order_detail_id = order_dict["id"]
            order_detail_obj = OrderDetail.get_one_order_detail(pk=order_detail_id)
            product_price = order_detail_obj.product.unit_price
            total_price = total_price + (quantity * product_price)

        data['company'] = Company.get_one_company(pk=data['company'])

        data.update({"total_amount": total_price,
                     "quantity": total_quantity})

        bill = Bill().create_bill(data=data)
        for i in challan_list:
            Challan.update_challan_for_bill(id=i, data={"bill": bill})

        bill_serializer = BillSerializer(bill).data
        return Response.create_data(bill_serializer)
    except Exception as err:
        # raise
        return Response.internal_server_error(str(err))


def update_bill_act(id=None, request=None):
    try:
        data = request.data
        data.update({"id": id})
        is_updated, bill = Bill().update_bill(type=data)
        if is_updated:
            bill_serializer = BillSerializer(bill).data
            return Response.create_data(bill_serializer, status=SUCCESS_STATUS_CODE)
        return Response.error(error_response=BILL_NOT_UPDATED, status=ERROR_STATUS_CODE)
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_bill(id):
    try:
        bill_obj = Bill().get_one_bill(pk=id)
        payment_time = bill_obj.company.payment_terms
        bill_date = datetime.strptime(bill_obj.bill_date, '%d/%m/%Y')
        bill_date_test = (bill_date +
                          timedelta(days=payment_time)).date()
        if datetime.now().date() == bill_date_test:
            payment_status = 1
        if datetime.now().date() > bill_date_test:
            payment_status = 2
        if datetime.now().date() < bill_date_test:
            payment_status = 0
        bill_serializer = BillSerializer(bill_obj, many=False).data
        bill_serializer.update({'payment_status':payment_status})
        return Response.create_data(bill_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))


import mimetypes

from email.message import EmailMessage


def get_single_bill_download(id):
    try:

        list_challan = []
        bill = Bill().get_one_bill(pk=id)

        bill_serializer = BillSerializer(bill, many=False).data
        total_price_bill = 0
        for i in bill_serializer['challan']:
            dict_challan_for_bill = {}
            challan = dict(i)
            challan_id = challan['id']
            challan_quantity = challan['quantity']
            dict_challan_for_bill.update({"challan_id": challan_id})
            dict_challan_for_bill.update({"quantity": challan_quantity})
            challan_order = dict(challan['order_detail'])

            product = dict(challan_order['product'])
            product_name = product['name']
            product_price = product['unit_price']
            dict_challan_for_bill.update({"product_name": product_name})
            dict_challan_for_bill.update({"product_price": product_price})
            challan_total = (challan_quantity * product_price)
            dict_challan_for_bill.update({"challan_total": challan_total})
            total_price_bill = total_price_bill + challan_total
            list_challan.append(dict_challan_for_bill)

        path_for_challan = '/home/affansidd/Desktop/PewBill/adminFunctions/Bill/' + str(bill.company.name) + '_' + 'bill' + '_' + str(id) + '.pdf'

        content_for_pdf = templates.challan_template.challan_template_func(product_name=product_name)
        pdfkit.from_string(content_for_pdf, path_for_challan)

        # return Response.success("File has been downloaded")
        return Response.create_data({"chalan": list_challan,
                                     "bill_total": total_price_bill})

    except Exception as err:
        return Response.internal_server_error(str(err))


def get_single_bill_send_by_email(id):
    try:
        bill = Bill().get_one_bill(pk=id)
        content = "Please find the attached Bill"
        subject = "Bill"
        path_for_challan = '/home/affansidd/Desktop/PewBill/adminFunctions/Bill/' + str(bill.company.name) + '_' + 'bill' + '_' + str(bill.id) + '.pdf'
        name_file = str(bill.company.name) + '_' + 'bill' + '_' + str(bill.id) + '.pdf'
        if SendEmail.send_email(reciever="m.affan@codexnow.com", attachment=True, name="PewBill", subject=subject,
                                content=content,
                                file_name=path_for_challan,
                                name_file=name_file):
            return Response.success("Bill successfully sent on email")
        return Response.error("Error on sending Bill.")
    except Exception as err:
        return Response.internal_server_error(str(err))


def delete_bill(id):
    try:
        Bill().delete_single_bill(pk=id)
        return Response.success("item has been deleted")
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_check_quantity(order_detail_id):
    try:
        if OrderDetail().check_order_detail_by_id(id=order_detail_id):

            order_detail_obj = OrderDetail().get_one_order_detail(pk=order_detail_id)
            total_quantity = order_detail_obj.quantity

            list_challan = Challan.get_all_challan_by_order_id(pk=order_detail_id)
            total_quantity_sent = 0

            for item in list_challan:
                total_quantity_sent = total_quantity_sent + item.quantity

            percentage = float((total_quantity_sent / total_quantity) * 100)

            dict_data = {"total_quantiy": total_quantity,
                         "total_item_sent": total_quantity_sent,
                         "percent_completed": percentage}

            return Response.create_data(dict_data)
        return Response.error("The provided order_id is invalid")

    except Exception as err:
        print(err)
        return Response.internal_server_error(str(err))

def get_all_contact(company_id):
    try:
        contact = Contact().get_all_contact(company_id=company_id)
        contact_serializer = ContactSerializer(contact, many=True).data
        return contact_serializer
    except Exception as err:
        return Response.internal_server_error(str(err))

def create_employee_contact(data):
    try:
        data['company'] = Company.get_one_company(pk=data.get('company'))
        employee_contact = Contact.create_contact(data=data)
        contact_serializer = ContactSerializer(employee_contact).data
        return Response.create_data(contact_serializer)
    except Exception as err:
        return Response.internal_server_error(str(err))