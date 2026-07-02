from DBUtil import DBUtil

class QUERY_EXECUTION:

    def __init__(self):
        self.dbUtil = DBUtil()
        self.dbUtil.mysql_connect()

    def verify_select(self,sql):
        select_res = self.dbUtil.select(sql)