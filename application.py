import os

from flask import Flask
from werkzeug.exceptions import HTTPException

from common.utils.error import APIException
from common.utils.error_code import ServerError
from config import secret


class Application(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super(Application, self).__init__(import_name, template_folder=template_folder, static_folder=None,
                                          root_path=root_path)
        self.config.from_object(secret)


app = Application(__name__, template_folder=os.getcwd() + "/web/templates/", root_path=os.getcwd())


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 调试模式
        # log
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e
