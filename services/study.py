import datetime

from common.utils.database import DB
import common.utils.error_code as err
from services.user import UserServices


class StudyServices:

    def __init__(self):
        self.db = DB()

    def add_study_item(self, uid, course_id):
        course_id = int(course_id)
        sql = 'select * from study where course_id=%s and user_id=%s and dt=CURDATE()'
        result = self.db.execute_query(sql, (course_id, uid))
        if len(result) == 0:
            sql = 'insert into study(user_id,course_id,study_time,dt) values (%s,%s,%s,CURDATE())'
            row = self.db.execute_update(sql, (uid, course_id, 1))
            self.add_grade_table(uid, 1)
            return row
        if course_id != 1 and course_id != 2 and course_id != 3 and result[0]['study_time'] >= 30:
            raise err.Forbidden('本节课今天学时已满')

        if course_id == 1 or course_id == 2 or course_id == 3:
            d_time0 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + ' 8:20', '%Y-%m-%d %H:%M')
            d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + ' 10:15', '%Y-%m-%d %H:%M')
            d_time2 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + ' 14:20', '%Y-%m-%d %H:%M')
            d_time3 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + ' 15:30', '%Y-%m-%d %H:%M')
            now = datetime.datetime.now()
            if not ((d_time0 < now < d_time1) or (d_time2 < now < d_time3)):
                raise err.Forbidden

        new_time = result[0]['study_time'] + 1
        sql = 'update study set study_time=%s where user_id=%s and course_id=%s and dt=CURDATE()'
        row = self.db.execute_update(sql, (new_time, uid, course_id))
        self.add_grade_table(uid, 1)
        return row

    def add_grade_table(self, uid, study_time):
        class_id = UserServices().get_user_info(uid)['class_id']
        week = {
            1: 'mon',
            2: 'tue',
            3: 'wed',
            4: 'thu',
            5: 'fri',
            6: 'sat',
            7: 'sun'
        }
        dt = datetime.datetime.now().isocalendar()
        week = week[dt[2]]
        iso = dt[1]
        sql = "select * from week where user_id=%s and w=%s"
        result = self.db.execute_query(sql, (uid, iso))
        if len(result) == 0:
            sql = "insert into week(w, user_id, " + week + ",class_id) values (%s,%s,%s,%s)"
            self.db.execute_update(sql, (iso, uid, study_time, class_id))
            return
        new_study_time = result[0][week] + study_time
        sql = "update week set " + week + "=%s where w=%s and user_id=%s"
        self.db.execute_update(sql, (new_study_time, iso, uid))

    def get_week_info(self, class_id):
        sql = "SELECT \
    class.`class_name` as 班级,\
    user.`user_name` as 姓名,\
    week.mon as 周一,\
    week.tue as 周二,\
    week.wed as 周三,\
    week.thu as 周四,\
    week.fri as 周五,\
    week.sat as 周六,\
    week.sun as 周日 \
    FROM (week INNER JOIN `class` on `week`.`class_id` = `class`.`id`) \
    INNER JOIN user on week.`user_id` = `user`.uid where week.class_id=%s and week.w=%s"
        result = self.db.execute_query(sql, (class_id, datetime.datetime.now().isocalendar()[1]))
        return result
