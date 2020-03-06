from common.utils.database import DB
import common.utils.error_code as err


class UserServices:

    def __init__(self):
        self.db = DB()

    def get_login(self, user, pwd):
        sql = "select uid from user where phone=%s and pwd=%s"
        result = self.db.execute_query(sql, (user, pwd))
        if len(result) == 0:
            raise err.AuthFailed
        return result[0]['uid']

    def get_user_info(self, uid):
        sql = "select * from user where uid=%s"
        result = self.db.execute_query(sql, uid)
        return result[0]

    def get_user_time(self, uid):
        sql = "select sum(study.study_time) as total from study where user_id=%s"
        result = self.db.execute_query(sql, uid)
        return 0 if result[0]['total'] is None else result[0]['total']

    def add_user(self, user, pwd, phone, class_id):
        sql = "insert into user(user_name, pwd, phone, class_id) values (%s,%s,%s,%s)"
        try:
            result = self.db.execute_update(sql, (user, pwd, phone, class_id))
        except Exception as e:
            raise err.ParameterException(msg=repr(e))
        sql = "select uid from user where phone=%s"
        result = self.db.execute_query(sql, phone)
        return result[0]['uid']
