from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.organization.repository import (
    repos_gw_get_organization_info, repos_gw_get_organization_info_from_child,
    repos_gw_get_organization_info_from_parent
)


class CtrGWOrganization(BaseController):
    async def ctr_gw_get_organization_info(self):
        current_user = self.current_user
        gw_organization_info = self.call_repos(await repos_gw_get_organization_info(
            current_user=current_user
        ))

        organization_infos = gw_organization_info["selectOrgInfo_out"]["data_output"]["org_info"]

        return self.response(data=[dict(
            id=organization_info['org_id'],
            parent_id=organization_info['org_parent_id'],
            name=organization_info['org_name'],
            short_name=organization_info['org_short_name'],
            path=organization_info['org_path'],
            path_description=organization_info['org_path_des'],
            order_by=organization_info['order_by'],
            childs=get_child_organization(organization_info['org_child'])
        ) for organization_info in organization_infos])

    async def ctr_gw_get_organization_info_from_parent(self):
        current_user = self.current_user
        gw_get_organization_info_from_parent = self.call_repos(await repos_gw_get_organization_info_from_parent(
            current_user=current_user

        ))

        organization_info = gw_get_organization_info_from_parent["selectOrgInfoFromParent_out"]["data_output"][
            "org_info"]

        return self.response(data=dict(
            id=organization_info['org_id'],
            parent_id=organization_info['org_parent_id'],
            name=organization_info['org_name'],
            short_name=organization_info['org_short_name'],
            path=organization_info['org_path'],
            path_description=organization_info['org_path_des'],
            order_by=organization_info['order_by']
        ))

    async def ctr_gw_get_organization_info_from_child(self):
        current_user = self.current_user
        gw_get_organization_info_from_child = self.call_repos(await repos_gw_get_organization_info_from_child(
            current_user=current_user

        ))

        organization_infos = gw_get_organization_info_from_child["selectOrgInfoFromChild_out"]["data_output"][
            "org_info"]

        return self.response(data=[dict(
            id=organization_info['org_id'],
            parent_id=organization_info['org_parent_id'],
            name=organization_info['org_name'],
            short_name=organization_info['org_short_name'],
            path=organization_info['org_path'],
            path_description=organization_info['org_path_des'],
            order_by=organization_info['order_by']
        ) for organization_info in organization_infos])


def get_child_organization(childs):
    children = []
    for child in childs:
        children.append(dict(
            id=child['org_id'],
            parent_id=child['org_parent_id'],
            name=child['org_name'],
            short_name=child['org_short_name'],
            path=child['org_path'],
            path_description=child['org_path_des'],
            order_by=child['order_by'],
            childs=get_child_organization(child['org_child'])
        ))
    return children
