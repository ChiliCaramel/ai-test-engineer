from db_util import DBUtil

class TestQuery:

    def __init__(self,db_util):
        self.db = db_util
    
    
    def test_select(self):

        print("----开始测试查询----")

        select_sql = "select * from student"
        select_res = self.db.select(select_sql)

        if select_res:
            print(f"查询成功，获取到 {len(select_res)} 条数据")
        else:
            print("查询结果为空或失败")

        print("----查询结束----")
    

    def test_insert(self):

        print("----开始测试插入----")
        insert_sql = """
        INSERT INTO student (id,Name,Sex,Birth,Department,Address) 
        VALUES 
        (114, '李五', '男', '2001-02-02', '英文系', '上海市徐汇区')
        """
        self.db.insert(insert_sql)

        verify_insertion_sql = "select * from student where id = 114"
    
        if self.db.select(verify_insertion_sql):
            print("插入成功: 找到ID 为 114的数据")
        else:
            print("插入失败：未在数据库找到ID 为 114 的数据")
    
        print("----测试插入结束----")
    
    def test_update(self):

        print("----开始测试更新----")
        update_sql = "update student set Name = '王王' where id = 114"
        self.db.update(update_sql)

        verify_update_sql = "select stu.Name from student stu where id = 114"
        update_res = self.db.select(verify_update_sql)

        if update_res and update_res[0]['Name'] == '王王':
            print("更新成功: 李五的名称已经更新为 王王")
        else:
            print("更新失败：未匹配名字为 '王王' 的同学")
    
        print("----测试更新结束----")
    
    def test_delete(self):
        print("----开始测试删除----")
        delete_query = 'delete from student where id = 114'
        self.db.delete(delete_query)

        verify_delete_sql = 'select * from student where id = 114'
        delete_res = self.db.delete(verify_delete_sql)

        if not delete_res:
            print("删除成功：ID 为 114的数据库已不存在于student表")
        else:
            print("更新失败：查询到ID 为 114的数据")

        print("----测试删除结束----")
    
    def run_all_tests(self):

        print("------Start------")

        self.test_select()
        self.test_insert()
        self.test_update()
        self.test_delete()

        print("------Done-----")