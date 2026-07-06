from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse,StreamingHttpResponse
from learndjango import models
from django.db.models import Count, Max, Min, Avg
from pracdjango.decorator import rate_limit
from django.utils import timezone
import os
from django.contrib.auth import login,authenticate
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core import serializers


# Create your views here.
# 写业务逻辑

@require_http_methods(['GET'])
def foreign_select(request):
    
    # 从 Employee 查对应的 Department -> 相关外键查主表
    emp = models.Employee.objects.get(id=1)

    print(emp.department)
    print(emp.department.name)

    # 主表查有相关外键表  模型名_set
    employees = models.Department.objects.get(id=1).employee_set.all()
    print(employees)

    # 跨表过滤 
    employees = models.Employee.objects.filter(department__name='技术部').values()

    employess_data_json = serializers("json",employees)

    # 等用于：
    # SELECT learndjango_employee.*
    # FROM learndjango_employee
    # INNER JOIN learndjango_department 
    # ON learndjango_employee.department_id = learndjango_department.id
    # WHERE learndjango_department.name = '技术部'

    # select_related -> 相当于 JOIN 通过外键将两个表连接起来  正向，通过相关外键查主表（多对一）
    employees_2 = models.Employee.objects.select_related('department').all()
    print(employees_2)
    for emp in employees_2:
        print(emp.department.name)
    # -> 等用于
    # SELECT * FROM employee
    # LEFT JOIN department ON employee.department_id = department.id;
    
    # 如果不用 select_related ，会先查出所有的Employees 再依次去查Department，多次查询。性能不友好。

    # prefetch_related -> 两次查询 反向，通过主表查有相关外键的表（一对多）
    departments = models.Department.objects.prefetch_related("employee_set").all()

    for dept in departments:
        employees = dept.employee_set.all()
    
    # 等同于：SELECT * FROM department # SELECT * FROM employee WHERE department_id IN (1, 2, 3)
    # 如果不用prefetch_related 是不是就等于 ：
    # SELECT * FROM department
    # SELECT * FROM employee WHERE department_id =1 
    # SELECT * FROM employee WHERE department_id =2
    # SELECT * FROM employee WHERE department_id = 3
    # 如果不用prefetch_related dept.employee_set.all() 要查询多次，造成N+1问题即多次查询




@require_http_methods(['GET'])
def test_pagination(request):
    """
    test pagination and verify 惰性加载
    """
    students = models.Students.objects.filter(age=18).values()
    stu_exclude = models.Students.objects.exclude(age=18)
    stu_all = models.Students.objects.all()
    stu_vlist = models.Students.objects.values_list()

    # 惰性加载
    print(type(students)) # QuerySet
    print(type(stu_exclude))
    print(type(stu_all))
    print(type(stu_vlist))

    pagination = Paginator(students,10)

    print(pagination) 
    print(type(pagination))

    current_page = pagination.page(1)
    print(current_page)
    print(type(current_page))

    # 触发查询
    result = list(current_page)
    print(result)
    print(type(result))

    return JsonResponse({'Msg': 'check console'}, status=200)


@require_http_methods(['POST'])
def decryption(request):
    """
    校验接口合法性的接口
    """
    sessionid = request.POST.get('sessionid')
    response ={}
    sessionid_obj = Session.objects.all().values()

    # 校验sessionid 合法性 - 接口/网页取的sessionid 和 session表里的是否匹配
    sessionid_obj = Session.objects.filter(session_key=sessionid).values()

    if not sessionid_obj:
        response['code'] = 2
        response['Msg'] = 'Illegal sessionid'
        return JsonResponse(response,status = 401)
    
    response['code'] = 0
    response['Msg'] = 'Sessionid is valid.'
    return JsonResponse(response,status = 200)

"""
接口请求校验
1.登录，登录接口返回sessionid
2.前端拿到sessionid
3.前端后续做的每个请求都带上sessionid
4.后端拿前端传回来的sessionid，去进行合法性校验。
cookie - session：
cookie 是存在前端，session是服务端生成，而且每次登录都会重新生成。
session过多会对服务器的性能产生影响，（每次请求进来都需要查询session表，session越多，表里记录越多，导致请求时间变长，服务器压力变大）
session储存空间也会受到影响。（每个登录，都会有一条新的记录，数量大会大量占用数据库磁盘空间）

"""


@require_http_methods(["POST"])
def learn_login(request):
    """
    User login API
    :param username user's account
    :param pwd  password
    :param code:
        0:Login successfully
        1:Failed to login , server error
        2:incorrect username or password
    """
    # verify if user input account / pwd
    username= request.POST.get('username')
    pwd = request.POST.get('pwd')

    if not username or not pwd:
        return JsonResponse(
            {'Msg':'Username and pwd are mandatory info.'},
            status=400
            )

    # verify if account / pwd correct
    user = authenticate(username=username,password=pwd)

    # 如果用户名密码正确则返回一个对象；如果用户名密码错误，返回None
    # print(user)

    response = {}
    if user is None:
        response['code'] = 2
        response['Msg'] = 'Username or password error!'
        return JsonResponse(response,status = 401) # 401 认证失败
    
    # perform login
    # login() 返回None，无法判断是否成功或失败，但是失败会抛出异常，所以用try except来判断与捕获
    try:
        login(request,user)
        response['code'] = 0
        response['Msg'] = 'Login successfully.'
        return JsonResponse(response,status = 200)
    except Exception as e:
        response['code'] = 1
        response['Msg'] = 'Failed to login.'
        return JsonResponse(response,status = 500)


@require_http_methods(['POST'])
def upload_file(request):
    """
    upload file
    """
    # 文件内容临时存在内存里，不是直接存到磁盘
    file = request.FILES.get('file')

    ## TODO 
    # MEDIA_ROOT 是 Django 推荐的文件存储方式，把路径统一配置在 settings.py 里，不管在哪台机器上部署，只需要改 settings.py 一个地方就够了
    save_path = f'/Users/carazhang/Desktop/AI Test Engineer/{file.name}'

    # 这里才是把文件写入指定的磁盘路径
    with open(save_path,'wb') as f:
        f.write(file.read())

    return JsonResponse({'Msg': 'File uploaded successfully.'}, status=200)

@require_http_methods(['GET'])
def download_files(request,file_name):
    """
    General file download endpoint. 
    Supports pdf,png,excel,word,txt formats.
    """

    # support formats
    ALLOWED_EXTENSIONS = ['pdf', 'png', 'xlsx', 'xls', 'docx', 'doc', 'txt']

    #get file extensions
    ext = file_name.split(".")[-1].lower()

    if not ext in ALLOWED_EXTENSIONS:
        return JsonResponse(
            {"Msg":f'File type .{ext} is not supported.'},
            status =400
        )

    file_path = f"/Users/carazhang/Desktop/AI Test Engineer/{file_name}"

    response = StreamingHttpResponse(open(file_path,"rb"))
    response['Content-Type'] = "application/octet-stream"
    response['Content-Disposition'] = f"attachment;filename={file_name}"

    return response


@require_http_methods(['GET'])
def download_file(request):
    """
    文件下载
    """
    file_path = '/Users/carazhang/Desktop/AI Test Engineer/download_file.txt'

    response = StreamingHttpResponse(open(file_path,'rb'))
    
    # 告诉浏览器这个是下载文件
    response['content-type'] = "application/octet-stream"

    # 告诉浏览器下载之后将文件命名成啥样
    response['Content-Disposition'] = "attachment;filename=222.txt"

    return response

@require_http_methods(['POST'])
def create_user_info(request):
    """
    :param name: user's name
           age: user's age
           phone: user's phone number

    :return code:
        0: success , user created successfully
        1: User already exists.
        2: invalid parameter - name/age/phone
        3: internal server error
    """
    response = {}
    
    name = request.POST.get('name')
    age = request.POST.get('age')
    phone = request.POST.get('phone')

    if not name:
        response['code']=2
        response["Msg"] = "Please provide a name."
        return JsonResponse(response,status=400)
    elif not age:
        response['code']=2
        response["Msg"] = "Please provide an age."
        return JsonResponse(response,status=400)
    elif not phone:
        response['code']=2
        response["Msg"] = "Please provide a phone."
        return JsonResponse(response,status=400)
    
    try:
        stu_info,created = models.Students.objects.get_or_create(
            name=name,
            age=age,
            phone=phone
        )
    except Exception as e:
        response['code']=3
        response['Msg']="Internal server error."
        return JsonResponse(response,status=500)
    
    if not created:
        response['code']=1
        response['Msg']="User already exists."
        return JsonResponse(response,status=409)
    
    if created:
        response['code']=0
        response['Msg']=f"User{stu_info.name} created successfully."
        return JsonResponse(response,status=200)
        


@require_http_methods(['GET'])
def get_user_info(request):
    """
    Get user info via phone.
    :param phone: user's phone number
    :return code:
        0: success , return user info
        1: user not found
        2: invalid parameter
        3: internal server error
    """
    
    response = {}
    phone = request.GET.get('phone')

    # 判断参数时候传入
    if not phone:
        response['code'] = 2
        response['Msg'] = 'Please provide a phone number.'
        return JsonResponse(response,status = 400)
    
    try:
        stu_obj = models.Students.objects.filter(phone=phone).values('name','age')
    except Exception as e:
        response['code'] = 3
        response['Msg'] = 'Internal server error.'
        return JsonResponse(response, status=500)
    
    # user doesn't exist
    if not stu_obj:
        response['code'] = 1
        response['Msg'] = "User not found."
        return JsonResponse(response, status=404)

    if stu_obj:
        response['code'] = 0 
        response['Msg'] = list(stu_obj)
    
    return JsonResponse(response, status=200) 


@require_http_methods(['POST'])
def maintain_student(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')

    stu_obj,created = (models.Students.objects
                         .update_or_create(
                            name=name,
                            defaults={"phone":phone}
                        )
    )

    if not created:
        return JsonResponse(
            {'Msg':f'phone {stu_obj.phone} updated'},
            status = 200
        )

    return JsonResponse(
        {'Msg':"New entry created."},
        status = 200
    )

"""
总结：
1. get_or_create 返回（object,True) -> 无数据，新建条目，(object,false)->有数据，不用新建
   get_or_create(teacher_nm=teacher_nm,c_name=c_name) -> 有就查询，无就根据这些条件创建。 如果创建条目多余查询条件就需要用 defaulsts={}

2. update_or_create 返回（object，True) -> 无数据，新建条目，(object,false)->有数据，不用新建，更新数据
    stu_obj,created = (models.Students.objects
                         .update_or_create(
                            name=name,    --> 查询条件
                            defaults={"phone":phone} -> 找到了就根据defaults里的条件更新，无没有找到就根据条件+defaults创建

                        )
    )


3. 关于defaults的规则：
如果column限定了 NOT NULL且没有默认值，则defaults中必须声明。
如果业务中需要指定初始值，则最好声明。

4. 前面的作业IPRequestLog为什么不采用update_or_create 的思考：
update_or_create 找到了会直接更新，但是在那个场景中，如果找到了数据需要先判断request_count是否已经超限制。如果直接用update_or_create 找到就更新了，统计超限逻辑会报错。
"""


@require_http_methods(['POST'])
def maintain_teacher(request):
    teacher_nm = request.POST.get('teacher_nm')
    c_name = request.POST.get('c_name')

    teacher_obj,created = (models.Teacher.objects
                         .get_or_create(
                            teacher_nm=teacher_nm,
                            c_name=c_name
                         )
    )

    if not created:
        return JsonResponse(
            {'Msg':f'The teacher already link to course-{teacher_obj.c_name}'},
            status = 429
        )

    return JsonResponse(
        {'Msg':"New entry is created."},
        status = 200
    )

@require_http_methods(['PATCH'])
def update_student_info(request):
    name = request.GET.get('name')
    age = 20
    create_time = timezone.now()
    # 可以用django 的 timezone.now() （截取到秒）更改DateTime类型的数据
    # timezone.now().date() 是截取到日
    if not name:
        return JsonResponse(
            {'msg':'name is mandatory'},
            status = 400
        )
    update_count = (models.Students.objects
                    .filter(name=name)
                    .update(create_time=create_time,age=age))

    if update_count ==0:
        return JsonResponse(
            {'msg':f'can not find {name}'},
            status = 404
        )
    else:
        return JsonResponse(
        {'msg':f'{name} info is updated.'},
        status = 200
    )

@require_http_methods(['DELETE'])
def delete_teacher_info(request):

    t_id = request.GET.get('t_id')

    if not t_id:
        return JsonResponse(
            {'msg':'t_id is mandatory'},
            status = 400
        )
    
    if not t_id.isdigit():
        return JsonResponse(
            {'msg':'please input positive number'},
            status = 400
        )
    # delete 返回的是元组
    deleted_count,teacher_obj = models.Teacher.objects.filter(t_id=t_id).delete()
    
    if deleted_count ==0:
        return JsonResponse(
            {'msg':f'can not find {t_id}'},
            status = 404
        )
    else:
        return JsonResponse(
        {'msg':f'{t_id} info is deleted.'},
        status = 200
    )

@require_http_methods(['POST'])
def create_teacher_info(request):

    teacher_nm = request.POST.get('teacher_nm')
    c_name = request.POST.get('c_name')

    if teacher_nm and c_name:
        teacher_obj = models.Teacher.objects.create(teacher_nm=teacher_nm,c_name=c_name)
        print(teacher_nm,c_name)
    else:
        return JsonResponse(
            {'msg':'Missing mandatory columns.'},
            status = 400
        )

    return JsonResponse(
        {'msg':f'{teacher_obj} info is created.'}
    )

# 代表调用请求时，请求方法必须为GET请求
# @require_http_methods(["GET"])
# def all_stu_info(request):
#     """
#     Docstring for all_stu_info
#     查询所有学员的信息
#     @age 学生的年龄
#     @return code 0 信息获取成功；1 信息获取失败
#     @return msg 返回所有学员的信息  学员信息不存在
#     """
#     response = {}
#     # 获取前端传参
#     age = request.GET.get('age') 
#     name = request.GET.get('name')
    
#     if not age:
#         response['code'] = 2
#         response['msg'] = 'age is None'
    
#     if int(age) ==1 :   # {"code": 0, "msg": "All Student Info"}
#         response['code'] = 0
#         response['msg'] = 'All Student Info'
#     if int(age) == 2:
#         response['code'] = 1
#         response['msg'] = 'All Student Info'
  
#     return JsonResponse(response) # 返回Json格式的response

@require_http_methods(['GET'])
def all_stu_info(request):
    """
    Get all student information
    @age 学员性别
    @return code 0 信息获取成功 1 信息获取失败 2 没有传入age参数
    @return msg 返回所有学员信息 ；学员信息不存在
    """
    response = {}
    # 获取students表里的所有数据
    # student_obj = models.Students.objects.all().values()
    # print(student_obj)
    # for stu in student_obj:
    #     print(stu)
    student_obj = models.Students.objects.filter(name='zhangsan').values('id','name')

    response['code'] = 0
    response['msg'] = list(student_obj) # 先转成list再返回，否则Json报错

    return JsonResponse(response)



@require_http_methods(["POST"])
def create_stu_info(request):
    """
    Docstring for create_stu_info
    :param request: Description
    @return code 0 创建成功 1 创建失败
    @return msg  created, failed
    """
    response = {}
    # 获取前端传参
    # age = request.POST.get('age')

    # # request.META
    # meta_info = request.META
    # print("-"*60)
    # print(meta_info) # 客户端请求的时候带过来的信息,字典格式
    # print(f"USER {meta_info['USER']}")
    # print(f"COLORTEAM {meta_info['COLORTERM']}")
    # print(f"VSCODE_INJECTION {meta_info['VSCODE_INJECTION']}")
    # print("-"*60)

    # if not age:
    #     response['code'] = 2
    #     response['msg'] = "student age is None"
    # else:
    #     response['code'] = 0
    #     response['msg'] = f"student age is {age}"
    name = 'wangwu'
    age = 18
    phone = 1312534456

    student_obj = models.Students.objects.create(name=name,age=age,phone=phone)


  
    return JsonResponse(
        {'msg': str(student_obj)}
    ) # 返回默认返回数据

@require_http_methods(['GET'])
def uniq_stu_info(request):

    name = request.GET.get('name')

    stu_info = models.Students.objects.filter(name=name).values()

    return JsonResponse(
        {'msg':list(stu_info)},
        status = 200
    )

@require_http_methods(['GET'])
def get_stu_score(request):

    stu_id = request.GET.get('stu_id')

    stu_scores = models.Score.objects.filter(stu_id=stu_id).values()

    return JsonResponse(
        {'msg':list(stu_scores)},
        status = 200
    )

@require_http_methods(['GET'])
def get_stu_age(request):

    name = request.GET.get('name')

    stu_scores = models.Students.objects.filter(name=name).values('age')

    return JsonResponse(
        {'msg':list(stu_scores)},
        status = 200
    )

@require_http_methods(['GET'])
def get_course_name(request):

    id = request.GET.get('id')

    c_name = models.Course.objects.filter(id=id).values()

    return JsonResponse(
        {'msg': list(c_name)},
        status = 200
    )

@require_http_methods(['GET'])
def get_all_courses(request):

    courses = models.Course.objects.all().values()
    return JsonResponse(
        {'msg':list(courses)},
        status = 200
    )

@require_http_methods(['POST'])
def get_phone_num(request):
    name = request.POST.get('name')
    age = request.POST.get('age')

    phone_Num = models.Students.objects.filter(name=name,age=age).values('phone')
    
    return JsonResponse(
        {'msg':list(phone_Num)},
        status = 200
    )


@require_http_methods(['POST'])
def get_same_age_stu(request):
    age = request.POST.get('age')

    students = models.Students.objects.filter(age=age).values('name')

    return JsonResponse(
        {'msg':list(students)},
        status = 200
    )

@require_http_methods(['POST'])
def get_course_score(request):
    c_name = request.POST.get('c_name')

    scores = models.Score.objects.filter(c_name=c_name).values('c_name','score')
        
    return JsonResponse(
        {'msg': list(scores)},
        status = 200
    )
@rate_limit(requests_per_day=4)
@require_http_methods(['POST'])
def get_stu_course(request):
    stu_id = request.POST.get('stu_id')

    courses = models.Score.objects.filter(stu_id=stu_id).values('c_name')
        
    return JsonResponse(
        {'msg': list(courses)},
        status = 200
    )

@require_http_methods(['POST'])
def get_avg_age(request):
    
    # age = request.POST.get('age')

    avg_age = models.Students.objects.aggregate(Avg('age'))
        
    return JsonResponse(
        {'msg': avg_age},
        status = 200
    )
    
