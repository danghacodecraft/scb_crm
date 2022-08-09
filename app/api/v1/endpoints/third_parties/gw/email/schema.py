def open_ebank_failure_response(customers, email_templates, template_key):
    """
        1. Email trong trường hợp phê duyệt trạng thái Chờ hậu kiểm / cần xác minh sang Không hợp lệ
    """
    title = "Thông báo V/v xác minh thông tin mở Tài khoản trực tuyến tại SCB."
    list_customer = ""
    if isinstance(customers, list):
        for customer in customers:
            list_customer += f"""{customer}{',' if customer != customers[-1] else ''} """
    else:
        list_customer = customers
    data = ""
    for key, value in email_templates.items():
        if 'open_ebank_failure_response' in key:
            data = value
            break

    first_data = data[:data.find(template_key)]
    last_data = data[data.rfind(template_key) + len(template_key):]
    data = first_data + list_customer + last_data

    return {"title": title, "data": data}


def open_ebank_success_response(customers, email_templates, template_key):
    """
    2. Email trong trường hợp phê duyệt trạng thái Không hợp lệ sang Hợp lệ
    """
    title = "Thông báo V/v Tài khoản trực tuyến tại SCB kích hoạt thành công."

    list_customer = ""
    if isinstance(customers, list):
        for customer in customers:
            list_customer += f"""{customer}{',' if customer != customers[-1] else ''} """
    else:
        list_customer = customers
    data = ""
    for key, value in email_templates.items():
        if 'open_ebank_success_response' in key:
            data = value
            break

    first_index = data.find(template_key)
    last_index = data.rfind(template_key)

    data = data[: first_index] + list_customer + data[last_index + len(template_key):]
    return {"title": title, "data": data}
