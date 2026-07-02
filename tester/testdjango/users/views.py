from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from users import models
from django.contrib.auth import login,authenticate
from django.contrib.sessions.models import Session

# Create your views here.

@require_http_methods(['POST'])
def check_auth(request):
    """
    Verify if the session is valid.
    :param sessionid: user's session id
    :return code:
        0: session is valid
        2: invalid or missing sessionid
    """
     
    sessionid = request.POST.get('sessionid')
    if not sessionid:
        return JsonResponse({'Msg': 'Please provide sessionid.'}, status=400)

    response={}
    
    sessionid_obj =  Session.objects.filter(session_key=sessionid).values()

    if not sessionid_obj:
        response['code'] = 2
        response['Msg'] = 'Illegal sessionid'
        return JsonResponse(response,status = 401)
    response['code'] = 0
    response['Msg'] = 'Sessionid is valid.'
    return JsonResponse(response,status = 200)


@require_http_methods(['POST'])
def user_login(request):
    """
    User session table for single sign-on.
    :param username user's account
    :param password  password
    :param code:
        0:Login successfully
        1:Failed to login , server error
        2:incorrect username or password
    """

    username = request.POST.get('username')
    password = request.POST.get('password')
    print(f"view 收到: username={username}, password={password}")

    if not username or not password:
        return JsonResponse(
            {'Msg':'Username and password are mandatory info.'},
            status=400
            )
    
    # verify if account / pwd correct
    user = authenticate(username=username,password=password)
    
    response = {}
    if user is None:
        response['code'] = 2
        response['Msg'] = 'Username or password error!'
        return JsonResponse(response,status = 401)
    
    try:
        models.UserSession.objects.filter(user=user).delete()
            
        login(request,user)
        session_key = request.session.session_key
        # print(f"session_key: {session_key}") 
        

        session_obj = Session.objects.get(session_key=session_key)
        # print(f"session_obj: {session_obj}")

        models.UserSession.objects.create(
            user=user,  # 因为创建了外键，外键字段存的是对象，所以不能用username ， 会报错 期望的是对象，但是给的字符串
            session=session_obj # 同上
        )
        """
        无bug版本写法，先查询，再删django表的记录，再删usersession表的记录
        old_session = models.UserSession.objects.filter(user=user).first()

        if old_session:
            # 第二步：通过外键拿到关联的 Session 对象，删除它
            old_session.session.delete()  # ✅ 删除 Django Session 表的记录（真正失效）
            old_session.delete()          # ✅ 删除 UserSession 表的记录

        这样能保证单点登录，比如A登录了电脑又通过手机再次上线，A的电脑session是被清理的，仅允许手机在线。
        同理，A登录后，换B登录，A的session会被清理
        核心：同一个账号同一时间只允许一个 session 存在
        """

        response['code'] = 0
        response['Msg'] = 'Login successfully.'
        return JsonResponse(response,status = 200)
    
    except Exception as e:
        # print(f"Error: {e}") 
        response['code'] = 1
        response['Msg'] = 'Failed to login.'
        return JsonResponse(response,status = 500)
        

@require_http_methods(['GET'])
def get_user_all_content(request):
    """
    Get user's all posted content by user_id 
    :param user_id: user's unique id
    :return code:
        0: success , return user_id , content and created_time
        1: user not found
        2: invalid parameter
        3: internal server error
    """
    response = {}
    user_id = request.GET.get('user_id')

    # verify if user_id provided
    if not user_id:
        response['code'] = 2
        response['Msg'] = 'Please provide a user_id.'
        return JsonResponse(response,status=400)
    
    try:
        content_detail = models.Post.objects.filter(user_id=user_id).values()
        print(type(content_detail))
    except Exception as e:
        response['code'] = 3
        response['Msg'] = 'Internal server error.'
        return JsonResponse(response,status=500)
    
    if not content_detail:
        response['code']=1
        response['Msg']='User not found.'
        return JsonResponse(response,status=404)
    
    if content_detail:
        response['code']=0
        response['Msg']= list(content_detail)
        return JsonResponse(response,status=200)
