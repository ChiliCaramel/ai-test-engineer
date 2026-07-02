import pymysql
import xlwt
import datetime
from decorator import timer

@timer
def write_to_excel():
    host = '124.223.193.254' # 数据库ip地址
    user = 'root' # 连接数据库的用户名
    port = 3306 # 连接数据库的端口号
    password = 'Cara@8888' #连接数据库的密码
    database = 'mysql' #连接的是哪个数据库
    charset = 'utf8' # 编码格式

    db_connect = pymysql.connect(host=host,user=user,port=port,password=password,database=database,charset=charset)
    cursor = db_connect.cursor(cursor=pymysql.cursors.DictCursor)

    get_all_stu = "select * from student"

    cursor.execute(get_all_stu)
    students = cursor.fetchall()

    # print(type(students))
    # print(students)

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Student_Info")

    # 写入表头
    headers = list(students[0].keys())

    for col_index,title in enumerate(headers):
        sheet.write(0,col_index,title)


    # 开始写入数据

    # 遍历所有学生
    for row_index,stu in enumerate(students,start = 1): # 第一行是表头
        # 遍历每一个学生的信息
        for col_index,value in enumerate(stu.values()):
        
            if isinstance(value,datetime.datetime):
                value = value.strftime("%Y-%m-%d") # 小写才是月份
            sheet.write(row_index,col_index,value)

    workbook.save("students.xls")
    print("Saved students complete.")

if __name__ == "__main__":
    write_to_excel()