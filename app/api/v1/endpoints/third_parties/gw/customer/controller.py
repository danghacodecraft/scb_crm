from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_gw_get_customer_info_detail, repos_gw_get_customer_info_list
)


class CtrGWCustomer(BaseController):
    async def ctr_gw_get_customer_info_list(
            self,
            cif_number: str,
            identity_number: str,
            mobile_number: str,
            full_name: str
    ):
        current_user = self.current_user
        customer_info_list = self.call_repos(await repos_gw_get_customer_info_list(
            cif_number=cif_number,
            identity_number=identity_number,
            mobile_number=mobile_number,
            full_name=full_name,
            current_user=current_user
        ))
        response_data = {}
        customer_list = customer_info_list["selectCustomerRefDataMgmtCIFNum_out"]["data_output"]["customer_list"]

        customer_list_info = []

        for customer in customer_list:
            customer_info = customer["customer_info_item"]['customer_info']
            cif_info = customer_info['cif_info']
            id_info = customer_info['id_info']
            address_info = customer_info['address_info']
            branch_info = customer_info['branch_info']

            customer_list_info.append(dict(
                fullname_vn=customer_info['full_name'],
                date_of_birth=customer_info['birthday'],
                martial_status=customer_info['martial_status'],
                gender=customer_info['gender'],
                email=customer_info['email'],
                nationality_code=customer_info['nationality_code'],
                mobile_phone=customer_info['mobile_phone'],
                telephone=customer_info['telephone'],
                otherphone=customer_info['otherphone'],
                customer_type=customer_info['customer_type'],
                cif_info=dict(
                    cif_number=cif_info['cif_num'],
                    issued_date=cif_info['cif_issued_date']
                ),
                id_info=dict(
                    number=id_info['id_num'],
                    name=id_info['id_name'],
                    issued_date=id_info['id_issued_date'],
                    expired_date=id_info['id_expired_date'],
                    place_of_issue=id_info['id_issued_location']
                ),
                address_info=dict(
                    address_full=address_info['address_full']
                ),
                branch_info=dict(
                    name=branch_info['branch_name'],
                    code=branch_info['branch_code'],
                )
            ))

        response_data.update({
            "customer_info_list": customer_list_info,
            "total_items": len(customer_list_info)
        })

        return self.response(data=response_data)

    async def ctr_gw_get_customer_info_detail(self, cif_number: str):
        current_user = self.current_user
        customer_info_detail = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number, current_user=current_user))

        customer_info = customer_info_detail['retrieveCustomerRefDataMgmt_out']['data_output']['customer_info']

        cif_info = customer_info['cif_info']
        id_info = customer_info['id_info']
        address_info = customer_info['address_info']
        job_info = customer_info['job_info']
        branch_info = customer_info['branch_info']

        return self.response(data=dict(
            fullname_vn=customer_info['full_name'],
            short_name=customer_info['short_name'],
            date_of_birth=customer_info['birthday'],
            martial_status=customer_info['martial_status'],
            gender=customer_info['gender'],
            email=customer_info['email'],
            nationality_code=customer_info['nationality_code'],
            mobile_phone=customer_info['mobile_phone'],
            telephone=customer_info['telephone'],
            otherphone=customer_info['otherphone'],
            customer_type=customer_info['customer_type'],
            resident_status=customer_info['resident_status'],
            legal_representativeprsn_name=customer_info['legal_representativeprsn_name'],
            legal_representativeprsn_id=customer_info['legal_representativeprsn_id'],
            biz_contact_person_phone_num=customer_info['biz_contact_person_phone_num'],
            biz_line=customer_info['biz_line'],
            biz_license_issue_date=customer_info['biz_license_issue_date'],
            is_staff=customer_info['is_staff'],
            cif_info=dict(
                cif_number=cif_info["cif_num"],
                issued_date=cif_info["cif_issued_date"]
            ),
            id_info=dict(
                number=id_info["id_num"],
                name=id_info["id_name"],
                issued_date=id_info["id_issued_date"],
                expired_date=id_info["id_expired_date"],
                place_of_issue=id_info["id_issued_location"]
            ),
            address_info=dict(
                address_full=address_info["address_full"],
                contact_address_full=address_info["contact_address_full"],
            ),
            job_info=dict(
                name=job_info["professional_name"],
                code=job_info["professional_code"]
            ),
            branch_info=dict(
                name=branch_info["branch_name"],
                code=branch_info["branch_code"]
            )
        ))

    async def ctr_gw_check_exist_customer_detail_info(
        self,
        cif_number: str
    ):
        gw_check_exist_customer_detail_info = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number,
            current_user=self.current_user
        ))
        customer_info = gw_check_exist_customer_detail_info['retrieveCustomerRefDataMgmt_out']['data_output']['customer_info'][
            'id_info']

        return self.response(data=dict(
            is_existed=True if customer_info['id_num'] else False
        ))
