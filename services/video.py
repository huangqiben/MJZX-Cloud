from common.utils.database import DB


class VideoServices:

    def __init__(self):
        self.db = DB()

    def get_video_info(self, vid):
        sql = "select * from course where id=%s order by id"
        result = self.db.execute_query(sql, vid)
        sql = "update course set watch=%s where id=%s"
        row = self.db.execute_update(sql, (result[0]['watch'] + 1, vid))
        return result[0]

    def get_video_list(self, subject_id):
        sql = "select * from course where subject_id=%s order by create_time desc"
        result = self.db.execute_query(sql, subject_id)
        return result
