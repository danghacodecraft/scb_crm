from app.api.base.controller import BaseController


class CtrSenderInfo(BaseController):
    async def ctr_sender_info(self, sender_request):
        cif_flag = sender_request.cif_flag
        if cif_flag:
            sender_info = {
                "cif_flag": sender_request.cif_flag,
                "cif_number": sender_request.cif_number,
                "note": sender_request.note
            }
        else:
            sender_info = {
                "cif_flag": sender_request.cif_flag,
                "fullname_vn": sender_request.fullname_vn,
                "identity": sender_request.identity,
                "issued_date": sender_request.identity,
                "place_of_issue": sender_request.place_of_issue,
                "address_full": sender_request.address_full,
                "mobile_phone": sender_request.mobile_phone,
                "note": sender_request.note
            }

        return sender_info
