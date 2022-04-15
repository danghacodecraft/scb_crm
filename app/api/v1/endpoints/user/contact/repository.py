from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repo_contact(code: str, session: Session):
    sql_contact = f"""SELECT HRM_EMPLOYEE.EMP_NAME,\
       HRM_EMPLOYEE.EMP_CODE,\
       HRM_EMPLOYEE.USERNAME,\
       HRM_EMPLOYEE.WORKING_LOCATION,\
       HRM_EMPLOYEE.EMAIL_SCB,\
       HRM_EMPLOYEE.CONTACT_MOBILE,\
       HRM_EMPLOYEE.INTERNAL_MOBILE,\
       HRM_EMPLOYEE.ID      AS EMP_ID,\
       HRM_TITLE.TITLE_NAME  AS TITLE_NAME,\
       HRM_ORGANIZATION.DESCRIPTION_PATH     AS UNIT,\
       CONCAT('/cdn-profile/', HRM_EMPLOYEE.AVATAR_URL) AS AVATAR_LINK FROM HRM_EMPLOYEE\

        LEFT OUTER JOIN HRM_TITLE ON (HRM_EMPLOYEE.TITLE_ID = HRM_TITLE.ID)
        LEFT OUTER JOIN HRM_ORGANIZATION ON (HRM_EMPLOYEE.ORG_ID = HRM_ORGANIZATION.ID)
        WHERE HRM_EMPLOYEE.EMP_CODE = {code}
        ORDER BY HRM_EMPLOYEE.USERNAME ASC"""

    data_contact = session.execute(sql_contact).one()
    return ReposReturn(data=data_contact)
