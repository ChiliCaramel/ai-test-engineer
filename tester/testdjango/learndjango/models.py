from django.db import models

# Create your models here.

# 设计数据库表结构

class Teacher(models.Model):

    t_id = models.AutoField(primary_key=True)
    # ALTER TABLE learndjango_teacher AUTO_INCREMENT = 701; 数据库跑一下，从701开始自增，Django只支持从1开始自增
    teacher_nm = models.CharField(max_length=64)
    c_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.teacher_nm} - {self.c_name}"


class Students(models.Model):
    """
    Docstring for Students
    学员管理表
    """
    id = models.AutoField(primary_key=True) # id 为字段名；AutoField = True 自增
    name = models.CharField(max_length=64,db_column='name') # CharField -> 数据库中字符类型；db_column -> 数据库字段
    age = models.IntegerField(default=0) # IntegerField -> 整型
    phone = models.CharField(default='',max_length=11,db_column='phone')
    create_time = models.DateTimeField(auto_now=True) # DateTimeField - YYYY-MM-DD HH:MM:SS DateField - YYYY-MM-DD auto_now -> 自动获取当前时间每次更新都会一起更新）

    """
    # 场景1：Python 变量名 和 数据库字段名 不一样时
    student_name = models.CharField(max_length=64, db_column='name')
    # Python 代码里用 student_name
    # 数据库里的列名是 name

    # 场景2：不写 db_column，默认和变量名一样
    name = models.CharField(max_length=64)
    # Python 代码里用 name
    # 数据库里的列名也是 name（默认）
    """

    def __str__(self):
        """
        Docstring for __unicode__
        :param self: Description
        配置默认的返回数据
        """
        return f"{self.id}, {self.name}"
    

class Score(models.Model):
    """
    成绩表
    """
    id = models.AutoField(primary_key=True)
    stu_id = models.IntegerField()
    c_name = models.CharField(max_length=64)
    score = models.FloatField()

    def __str__(self):
        return f"{self.stu_id} - {self.c_name} - {self.score}"

class Course(models.Model):
    """
    课程目录
    """
    id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id} - {self.c_name}"


