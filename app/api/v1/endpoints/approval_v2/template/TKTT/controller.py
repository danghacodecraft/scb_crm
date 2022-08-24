from app.api.base.controller import BaseController


class CtrTemplateTKTT(BaseController):
    async def ctr_get_template_nop_tien(self, object_data):
        data = {
            'S1.A.1.3.1': "",
            'S1.A.1.3.2': "",
            'S1.A.1.3.3': object_data.get('receiver', {}).get('bank_branch12', None),
            'S1.A.1.3.4': object_data.get('created_at', None),
            'S1.A.1.3.5': "",
            'S1.A.1.3.6': "",
            'S1.A.1.3.8': object_data.get('sender', {}).get('fullname_vn', None),
            'S1.A.1.3.12': "",
            'S1.A.1.3.13': object_data.get('transfer', {}).get('amount', None),
            'S1.A.1.3.14': object_data.get('fee_info', {}).get('amount', None),
            'S1.A.1.3.15': object_data.get('fee_info', {}).get('vat', None),
            'S1.A.1.3.16': object_data.get('transfer', {}).get('amount', None),
            'S1.A.1.3.17': object_data.get('transfer', {}).get('content', None),
            'S1.A.1.3.18': object_data.get('sender', {}).get('fullname_vn', None),
            'S1.A.1.3.19': object_data.get('sender', {}).get('mobile_phone', None),
            'S1.A.1.3.20': object_data.get('sender', {}).get('identity_info', {}).get('number', None),
            'S1.A.1.3.21': object_data.get('sender', {}).get('identity_info', {}).get('issued_date', None),
            'S1.A.1.3.22': object_data.get('sender', {}).get('identity_info', {}).get('place_of_issue', {}).get('name', None),
            'S1.A.1.3.23': object_data.get('sender', {}).get('address_full', None),
            'S1.A.1.3.7': "",
            'S1.A.1.3.9': object_data.get('statement', {}).get('statements', None),
            'S1.A.1.3.24': object_data.get('statement', {}).get('total', None),
            'S1.A.1.3.25': object_data.get('statement', {}).get('total_number_of_bills', None),
            'S1.A.1.3.26': object_data.get('created_by', None),
            'S1.A.1.3.27': ""
        }
        return data
