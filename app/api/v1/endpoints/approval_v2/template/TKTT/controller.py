# from app.api.base.controller import BaseController
#
#
# class CtrTemplateTKTT(BaseController):
#     async def ctr_get_template_nop_tien(self, object_data):
#         #
#         # list_data_in_group = []
#         # if object_data.get('statement', {}).get('statements',None):
#         #     for index, data_in_row in enumerate(object_data.get('statement', {}).get('statements',None)):
#         #         for key, value in data_in_row.items():
#         #             list_data_in_group.append({})
#         #     list_data_in_group = []
#         data = {
#             'S1.A.1.3.1': "",
#             'S1.A.1.3.2': "",
#             'S1.A.1.3.3': str(object_data.get('receiver', {}).get('bank_branch12', None)),
#             'S1.A.1.3.4': str(object_data.get('created_at', None)),
#             'S1.A.1.3.5': "",
#             'S1.A.1.3.6': "",
#             'S1.A.1.3.8': str(object_data.get('sender', {}).get('fullname_vn', None)),
#             'S1.A.1.3.12': "",
#             'S1.A.1.3.13': str(object_data.get('transfer', {}).get('amount', None)),
#             'S1.A.1.3.14': str(object_data.get('fee_info', {}).get('amount', None)),
#             'S1.A.1.3.15': str(object_data.get('fee_info', {}).get('vat', None)),
#             'S1.A.1.3.16': str(object_data.get('transfer', {}).get('amount', None)),
#             'S1.A.1.3.17': str(object_data.get('transfer', {}).get('content', None)),
#             'S1.A.1.3.18': str(object_data.get('sender', {}).get('fullname_vn', None)),
#             'S1.A.1.3.19': str(object_data.get('sender', {}).get('mobile_phone', None)),
#             'S1.A.1.3.20': str(object_data.get('sender', {}).get('identity_info', {}).get('number', None)),
#             'S1.A.1.3.21': str(object_data.get('sender', {}).get('identity_info', {}).get('issued_date', None)),
#             'S1.A.1.3.22': str(object_data.get('sender', {}).get('identity_info', {}).get('place_of_issue', {}).get('name', None)),
#             'S1.A.1.3.23': str(object_data.get('sender', {}).get('address_full', None)),
#             'S1.A.1.3.7': "",
#             'S1.A.1.3.9': object_data.get('statement', {}).get('statements',None),
#             'S1.A.1.3.24': str(object_data.get('statement', {}).get('total', None)),
#             'S1.A.1.3.25': str(object_data.get('statement', {}).get('total_number_of_bills', None)),
#             'S1.A.1.3.26': str(object_data.get('created_by', None)),
#             'S1.A.1.3.27': ""
#         }
#         return data
