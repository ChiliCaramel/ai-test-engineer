import xlrd
import pymysql
import datetime
from decorator import timer

@timer
def write_to_db():

    host = '124.223.193.254' # 数据库ip地址
    user = 'root' # 连接数据库的用户名
    port = 3306 # 连接数据库的端口号
    password = 'Cara@8888' #连接数据库的密码
    database = 'mysql' #连接的是哪个数据库
    charset = 'utf8' # 编码格式

    db_connect = pymysql.connect(host=host,user=user,port=port,password=password,database=database,charset=charset)
    cursor = db_connect.cursor(cursor=pymysql.cursors.DictCursor)

    workbook = xlrd.open_workbook("students.xls") # 记得改文件名
    sheet = workbook.sheet_by_name("New_StudentsInfo") # 记得改表名

    # 获取列名 (第0行)
    headers = sheet.row_values(0)
    col_names = ", ".join(headers) 

    # 从第1行开始循环数据
    for row_index in range(1, sheet.nrows):
        row_data = sheet.row_values(row_index)
    
        values_list = []
        for val in row_data:
            # 处理ID 一直报错说是浮点数 强制转换成int
            if isinstance(val, float) and val.is_integer():
                val = int(val)
            
            # 处理日期 一直报错是浮点数 查了资料可以做如下处理
            # 如果它是浮点数（例如 44633.0），且数值很大（大于1000），说明是 Excel 日期序列号
            elif isinstance(val, float) and val > 1000:
                try:
                    real_date = xlrd.xldate_as_datetime(val, workbook.datemode)
                    val = real_date.strftime('%Y-%m-%d') # 变成 '2022-03-13'
                except Exception:
                    pass
                
            # 拼接成‘张三’
            values_list.append("'" + str(val) + "'")
        
        values_str = ", ".join(values_list)
    
        insert_sql = f"INSERT INTO student ({col_names}) VALUES ({values_str})"
    
        try:
            cursor.execute(insert_sql)
            db_connect.commit()
        except Exception as e:
            print(f"第 {row_index} 行出错: {e}")
            print(f"SQL: {insert_sql}") 

    print("终于搞完了")

if __name__ == "__main__":
    write_to_db()