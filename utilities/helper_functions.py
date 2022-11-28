from pewbill.responses import Response

gross_price_list = {
    "LineText": "Gross Price",
    "Words": [
        {
            "WordText": "Gross",
            "Left": 24.0,
            "Top": 696.0,
            "Height": 13.0,
            "Width": 39.0
        },
        {
            "WordText": "Price",
            "Left": 63.0,
            "Top": 696.0,
            "Height": 13.0,
            "Width": 37.0
        }
    ],
    "MaxHeight": 14.0,
    "MinTop": 696.0
}
pkr_dict = {
    "LineText": "(PKR)",
    "Words": [
        {
            "WordText": "(",
            "Left": 650.0,
            "Top": 541.0,
            "Height": 15.0,
            "Width": 42.0
        },
        {
            "WordText": "PKR",
            "Left": 650.0,
            "Top": 540.0,
            "Height": 16.0,
            "Width": 42.0
        },
        {
            "WordText": ")",
            "Left": 650.0,
            "Top": 541.0,
            "Height": 15.0,
            "Width": 42.0
        }
    ],
    "MaxHeight": 16.0,
    "MinTop": 540.0
}


def get_po_data_for_k_electric(data):
    try:
        list_data_new = data['ParsedResults'][0]['TextOverlay']['Lines']

        gross_price_pos = list_data_new.index(gross_price_list)

        gross_pkr_dict_pos = list_data_new.index(pkr_dict)

        length_list = len(list_data_new)
        item_list = []
        for i in range(length_list):
            if gross_pkr_dict_pos < i < gross_price_pos:
                item_list.append(list_data_new[i])

        purchase_order_number = list_data_new[13]['LineText']
        purchase_order_date = list_data_new[16]['LineText']

        # delivery_date = list_data_new[56]['LineText'][-10::]
        quantity = 0

        for i in range(1, len(item_list), 8):
            quantity = quantity + int(item_list[i]['LineText'])

        company = 1
        total_amount = list_data_new[66]['LineText']

        dict_purchase_order = {"purchase_order_number": purchase_order_number,
                               "purchase_order_date": purchase_order_date,
                               # "delivery_date": delivery_date,
                               "quantity": quantity,
                               "company": company,
                               "total_amount": total_amount}

        return dict_purchase_order

    except Exception as err:
        return Response.internal_server_error(str(err))


def get_po_data_for_pel(data):
    try:
        pass
    except Exception as err:
        return Response.internal_server_error(str(err))


def get_po_data_for_elmetec(data):
    try:
        print("CCCCCCCCCCCCCCCCCCCCCC")

    except Exception as err:
        return Response.internal_server_error(str(err))


def get_po_data_for_transfopower(data):
    try:
        print("CCCCCCCCCCCCCCCCCCCCCC")

    except Exception as err:
        return Response.internal_server_error(str(err))


def get_po_data_for_skypower(data):
    try:
        print("CCCCCCCCCCCCCCCCCCCCCC")

    except Exception as err:
        return Response.internal_server_error(str(err))
