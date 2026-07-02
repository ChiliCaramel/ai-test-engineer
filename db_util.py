import pymysql


class DBUtil:

    def __init__(self):
        self.db_connect = None
        self.cursor = None

    def mysql_connect(self):

        host = '124.223.193.254' # 数据库ip地址
        user = 'root' # 连接数据库的用户名
        port = 3306 # 连接数据库的端口号
        password = 'Cara@8888' #连接数据库的密码
        database = 'mysql' #连接的是哪个数据库
        charset = 'utf8' # 编码格式

        try:
            # 连接数据库
            self.db_connect = pymysql.connect(host=host,user=user,port=port,password=password,database=database,charset=charset)

            # 创建一个可执行sql的光标
            self.cursor = self.db_connect.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            print(f"DB connection failed due to {e}")
    
    def select(self,sql):

        try:
            self.cursor.execute(sql)
            select_res = self.cursor.fetchall()
            
            return select_res
        except Exception as e:
            print(f"Select query failed execue failed, due to Exception{e}")
    
    def insert(self,sql):
        try:
            self.cursor.execute(sql)
            self.db_connect.commit()
        except Exception as e:
            self.db_connect.rollback()
            print(f"Insertion failed, due to Exception {e}")
    
    def update(self,sql):
        try:
            self.cursor.execute(sql)
            self.db_connect.commit()
        except Exception as e:
            self.db_connect.rollback()
            print(f"Update failed due to Exception {e}")
    
    def delete(self,sql):
        try:
            self.cursor.execute(sql)
            self.db_connect.commit()
        except Exception as e:
            self.db_connect.rollback()
            print(f"Delete failed due to Exception {e}")
    
    def close_DB_connection(self):
        self.cursor.close()
        self.db_connect.close()
        print("-----数据库操作完成，数据库连接已关闭-----")


if __name__ == "__main__":

    # 实例化DBUtile 并 连接DB
    dbUtil = DBUtil()

    try:
        dbUtil.mysql_connect()

        if not dbUtil.db_connect:
            print("DB未连接，无法进行以下测试")
        else:


            # 查询
            print("----开始测试查询----")
            select_sql = "select * from student"
            select_res = dbUtil.select(select_sql)
            print(f"查询结果：{select_res}")
            print("----查询结束----")

            # insert
            print("----开始测试插入----")
            insert_sql = """
            INSERT INTO student (id,Name,Sex,Birth,Department,Address) 
            VALUES 
            (114, '李五', '男', '2001-02-02', '英文系', '上海市徐汇区')
            """
            dbUtil.insert(insert_sql)

            verify_insertion_sql = "select * from student where id = 114"
    
            if dbUtil.select(verify_insertion_sql):
                print("插入成功: 找到ID 为 114的数据")
            else:
                print("插入失败：未在数据库找到ID 为 114 的数据")
    
            print("----测试插入结束----")

            # update
            print("----开始测试更新----")
            update_sql = "update student set Name = '王王' where id = 114"
            dbUtil.update(update_sql)

            verify_update_sql = "select stu.Name from student stu where id = 114"
            update_res = dbUtil.select(verify_update_sql)

            if update_res and update_res[0]['Name'] == '王王':
                print("更新成功: 李五的名称已经更新为 王王")
            else:
                print("更新失败：未匹配名字为 '王王' 的同学")
    
            print("----测试更新结束----")

            # delete
            print("----开始测试删除----")
            delete_query = 'delete from student where id = 114'
            dbUtil.delete(delete_query)

            verify_delete_sql = 'select * from student where id = 114'
            delete_res = dbUtil.delete(verify_delete_sql)

            if not delete_res:
                print("删除成功：ID 为 114的数据库已不存在于student表")
            else:
                print("更新失败：查询到ID 为 114的数据")

            print("----测试删除结束----")
    
    except Exception as e:
        print(f"测试过程中发生错误{e}")
    
    finally:
        # 关闭连接
        if dbUtil.db_connect:
            dbUtil.close_DB_connection()


    