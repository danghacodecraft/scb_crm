import codecs
import glob
import os

from loguru import logger

from app.utils.error_messages import ERROR_EMAIL_TEMPLATES_GW


def email_template_response():
    try:
        html_files = []
        for file in glob.glob(f"{os.path.abspath(os.getcwd())}/app/utils/email_templates/*.html"):
            html_files.append(file)
        if html_files:
            result = {}
            for html_file in html_files:
                file = codecs.open(html_file, 'r', encoding='utf-8')
                result[file.name] = file.read()
                file.close()

            return result
    except Exception as ex:
        logger.error(str(ex))
        return_error = dict(
            loc="EMAIL_TEMPLATES GW",
            msg=ERROR_EMAIL_TEMPLATES_GW,
            detail=ex
        )
        return return_error


EMAIL_TEMPLATES = email_template_response()
