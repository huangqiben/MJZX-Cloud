import pymysql
from config.secret import db_config


class DB:
    db_host = db_config['host']
    db_user = db_config['user']
    db_pass = db_config['pwd']
    db_database = db_config['database']
    db_port = db_config['post']

    def get_connection(self):
        return pymysql.connect(host=self.db_host, port=self.db_port, user=self.db_user, passwd=self.db_pass,
                               db=self.db_database, autocommit=True)

    def execute_query(self, sql, args=None):
        self.connection = self.get_connection()
        self.coursor = self.connection.cursor(pymysql.cursors.DictCursor)
        self.coursor.execute(sql, args)
        result = self.coursor.fetchall()
        self.coursor.close()
        self.connection.close()
        return result

    def execute_update(self, sql, args=None):
        self.connection = self.get_connection()
        self.coursor = self.connection.cursor()
        row = self.coursor.execute(sql, args)
        self.coursor.close()
        self.connection.close()
        return row
