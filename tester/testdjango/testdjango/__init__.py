import pymysql


"""
# Django 内部代码是 import MySQLdb  而目前我已经安装的是 pymysql 所以需要伪装一下
"""
pymysql.install_as_MySQLdb()

