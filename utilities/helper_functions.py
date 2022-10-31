from pewbill.responses import Response


def get_po_data_for_k_electric(data):
    try:
        print(data)
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