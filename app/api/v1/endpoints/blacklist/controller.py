from app.api.base.controller import BaseController
from app.api.v1.endpoints.blacklist.schema import BlacklistResponse
from app.api.v1.endpoints.blacklist.repository import repo_add_blacklist, repo_view_blacklist
from app.api.v1.dependencies.paging import PaginationParams
from typing import List
class CtrBlackList(BaseController):

    async def ctr_create_blacklist(self, data_blacklist:BlacklistResponse):

        data_insert = {
            'full_name' : data_blacklist.full_name ,
            'date_of_birth' : data_blacklist.date_of_birth ,
            'identity_id' : data_blacklist.identity_id ,
            'issued_date' : data_blacklist.issued_date ,
            'place_of_issue_id' : data_blacklist.place_of_issue_id ,
            'cif_num' : data_blacklist.cif_num ,
            'casa_account_num' : data_blacklist.casa_account_num ,
            'branch_id' : data_blacklist.branch_id ,
            'date_open_account_number' : data_blacklist.date_open_account_number ,
            'mobile_num' : data_blacklist.mobile_num ,
            'place_of_residence' : data_blacklist.place_of_residence ,
            'place_of_origin' : data_blacklist.place_of_origin ,
            'reason' : data_blacklist.reason ,
            'job_content' : data_blacklist.job_content ,
            'blacklist_source' : data_blacklist.blacklist_source ,
            'document_no' : data_blacklist.document_no ,
            'blacklist_area' : data_blacklist.blacklist_area ,
        }

        self.call_repos(await repo_add_blacklist(
                                data_blacklist=data_insert,
                                session=self.oracle_session
                                )
                        )
        return self.response(data={
            **data_insert
        })


    async def ctr_view_blacklist(self,
                                 pagination_params:PaginationParams,
                                 identity_id:List[str],
                                 # cif_num:str,
                                 # casa_account_num:str
                                 ):

        blacklist = self.call_repos(await repo_view_blacklist(
                                session=self.oracle_session,
                                limit=pagination_params.limit,
                                page=pagination_params.page,
                                identity_id=identity_id
                            )
                        )
        return blacklist