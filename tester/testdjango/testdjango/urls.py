"""testdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from learndjango import views as ld_views
from pracdjango import views as pd_views
from users import views as u_views
from blog import views as b_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('allStuInfo/',ld_views.all_stu_info), # 后续如果调用到allStuInfo 这个接口，就会自动执行 views.py 的all_stu_info方法
    path('createStuInfo/',ld_views.create_stu_info),
    path('uniqStuInfo/',ld_views.uniq_stu_info),
    path('stuScores/',ld_views.get_stu_score),
    path('getStuAge/',ld_views.get_stu_age),
    path('courseName/',ld_views.get_course_name),
    path('allCourses/',ld_views.get_all_courses),
    path('phoneNum/',ld_views.get_phone_num),
    path('sameAgeStu/',ld_views.get_same_age_stu),
    path('getCourseScore/',ld_views.get_course_score),
    path('getStuCourse/',ld_views.get_stu_course),
    path('getAvgAge/',ld_views.get_avg_age),
    path('verifyIPApplyCnt/',pd_views.requests_ip_addr),
    path('createTeacherandCourse/',ld_views.create_teacher_info),
    path('deleteTeacherInfo/',ld_views.delete_teacher_info),
    path('updateStudentInfo/',ld_views.update_student_info),
    path('maintainTeacherInfo/',ld_views.maintain_teacher),
    path('maintainStudentInfo/',ld_views.maintain_student),
    path('getUserInfo/',ld_views.get_user_info),
    path('getUserPostContent/',u_views.get_user_all_content),
    path('create-user-info/',ld_views.create_user_info),
    path('post-blog/',b_views.post_blog),
    path('download-file/',ld_views.download_file),
    path('download/<str:file_name>/',ld_views.download_files), # Django路径参数写法： <> 表示路径参数，str:file_name -> 类型：变量名
    path('upload-file/',ld_views.upload_file),
    path('learnLogin/',ld_views.learn_login),
    path('user-login/',u_views.user_login),
    path('test-pagination/',ld_views.test_pagination)
]
