from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.settings.event import service_gw


async def repos_gw_open_cards(current_user: UserInfoResponse,
                              cif_number: str = None,
                              card_info=None,
                              customer_info=None,
                              maker_staff_name: str = None,
                              data=None):
    data_input = {
        "sequenceNo": "2022061315025580",
        "fi": "970429",
        "srcSystm": "WSPORTAL",
        "cif_info": {
            "cif_num": cif_number
        },
        "account_info": {
            "account_type": "2"
        },
        "card_info": {
            "card_indicator": card_info.card_indicator if card_info else "",
            "card_type": card_info.card_type if card_info else "",
            "card_auto_renew": card_info.card_auto_renew if card_info else "",
            "card_release_form": card_info.card_release_form if card_info else "",
            "card_block_online_trans": card_info.card_block_online_trans if card_info else "",
            "card_contact_less": card_info.card_contact_less if card_info else "",
            "card_relation_to_primany": card_info.card_relation_to_primany if card_info else "",
            "card_mother_name": card_info.card_mother_name if card_info else "",
            "card_secure_question": card_info.card_secure_question if card_info else "",
            "card_bill_option": card_info.card_bill_option if card_info else "",
            "card_statement_delivery_option": card_info.card_statement_delivery_option if card_info else ""
        },
        "prinCrdNo": "",
        "customer_info": {
            "birthday": customer_info.birthday if customer_info else "",
            "title": customer_info.birthday if customer_info else "",
            "full_name_vn": customer_info.birthday if customer_info else "",
            "last_name": customer_info.birthday if customer_info else "",
            "first_name": customer_info.birthday if customer_info else "",
            "middle_name": customer_info.birthday if customer_info else "",
            "current_official": customer_info.birthday if customer_info else "",
            "embPhoto": customer_info.birthday if customer_info else "",
            "gender": customer_info.birthday if customer_info else "",
            "nationality": customer_info.birthday if customer_info else "",
            "martial_status": customer_info.birthday if customer_info else "",
            "resident_status": customer_info.birthday if customer_info else "",
            "mthToStay": customer_info.birthday if customer_info else "",
            "prStat": customer_info.birthday if customer_info else "",
            "vsExpDate": customer_info.birthday if customer_info else "",
            "education": customer_info.birthday if customer_info else "",
            "customer_type": customer_info.birthday if customer_info else ""
        },
        "id_info": {
            "id_name": "O",
            "id_num": "280844390",
            "id_num_by_cif": "",
            "id_issued_location": "BINH DUONG",
            "id_issued_date": "2014-08-06"
        },
        "srcCde": "DM412",
        "branch_issued": {
            "branhch_code": "000"
        },
        "direct_staff": {
            "staff_code": "19461"
        },
        "promoCde": "P404",
        "indirect_staff": {
            "staff_code": "12345"
        },
        "imgId": "12345",
        "contract_info": {
            "contract_name": ""
        },
        "resident_info": {
            "address_info": {
                "line": "927 TRAN HUNG DAO",
                "ward_name": "PHUONG 1",
                "contact_address_line": "",
                "city_code": "70",
                "district_name": "QUAN 5",
                "city_name": "TP HCM",
                "country_name": "VN",
                "telephone1": "0909101600"
            },
            "customer_info": {
                "resident_type": "O",
                "resident_since": "201411"
            }
        },
        "correspondence_info": {
            "address_info": {
                "line": "927 TRAN HUNG DAO",
                "ward_name": "PHUONG 1",
                "contact_address_line": "",
                "city_code": "70",
                "district_name": "QUAN 5",
                "city_name": "TP HCM",
                "country_name": "VN",
                "telephone1": "02815698630",
                "mobile_phone": "0909555800"
            },
            "smsInd": "Y",
            "email": "quanlt@scb.com.vn"
        },
        "office_info": {
            "customer_info": {
                "biz_line": "",
                "employee_nature": "",
                "cor_capital": "",
                "biz_position": "",
                "employee_since": "000000",
                "office_name": ""
            },
            "address_info": {
                "line": "927 TRAN HUNG DAO",
                "ward_name": "PHUONG 1",
                "contact_address_line": "",
                "city_code": "70",
                "district_name": "QUAN 5",
                "city_name": "TP HCM",
                "country_name": "VN",
                "telephone1": "0274333777",
                "phone_ext1": "805",
                "telephone2": "",
                "phone_ext2": "",
                "fax_no": ""
            }
        },
        "previous_employer_info": {
            "customer_info": {
                "office_name": "",
                "employee_since": "000000",
                "employee_duration": "0"
            },
            "address_info": {
                "line": "",
                "ward_name": "",
                "contact_address_line": "",
                "city_code": "",
                "district_name": "",
                "city_name": "",
                "country_name": "",
                "telephone1": "",
                "phone_ext1": ""
            }
        },
        "personal_details": {
            "ownHouseLand": "N",
            "ownCar": "N",
            "noOfDepen": "0",
            "avgSpendMth": "0",
            "bankPrd": "",
            "bankOthrPrd": "",
            "othrCCBankName": "",
            "othrCCLimit": "",
            "othrLoanBankName": "",
            "othrLoanInstallMth": "",
            "delivByBrchInd": "Y",
            "delivOpt": "O"
        },
        "delivery_info": {
            "address_info": {
                "line": "927 TRAN HUNG DAO",
                "ward_name": "PHUONG 1",
                "contact_address_line": "",
                "city_code": "70",
                "district_name": "QUAN 5",
                "city_name": "TP HCM",
                "country_name": "VN"
            },
            "delivBrchId": "SGN"
        },
        "spouse_company_info": {
            "spcName": "",
            "spcIdInd": "",
            "spcNewId": "",
            "spcEmpName": "",
            "address_info": {
                "line": "927 TRAN HUNG DAO",
                "ward_name": "PHUONG 1",
                "contact_address_line": "",
                "city_code": "70",
                "district_name": "QUAN 5",
                "city_name": "TP HCM",
                "country_name": "VN",
                "telephone1": "",
                "phone_ext1": ""
            },
            "spcEmpPosi": "",
            "spcEmpSince": "000000",
            "spcEmpWorkNat": "S"
        },
        "emergency_info": {
            "emerContcPrsn": "TRAN VAN DANG",
            "emerGender": "M",
            "emerPhoneNo": "0908555999",
            "emerMobileNo": "0909555866",
            "emerRelt": "O"
        },
        "card_addon_data": {
            "payMeth": "0",
            "payCASA": "0",
            "payAmt": "0",
            "casaAcctNo": "1370106438990001",
            "casaAcctTyp": "20",
            "casaCurCde": "704",
            "recomCrdNo": "",
            "recomName": "",
            "remark": "",
            "apprvDeviation": "NOTE",
            "addData1": "",
            "addData2": "",
            "smsInfo": "0",
            "narrative": "CRM WS",
            "attachment": "",
            "decsnStat": "AM"
        },
        "checker_info": {
            "staff_code": current_user.username
        },
        "approver_info": {
            "staff_code": "HOANND2"
        }
    }

    gw_open_cards = await service_gw.open_cards(
        current_user=current_user,
        data_input=data if data else data_input
    )
    return ReposReturn(data=gw_open_cards)
