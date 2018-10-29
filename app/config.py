import os

DEBUG = True
SECRET_KEY = os.urandom(24)

# 数据库配置
HOSTNAME = '211.159.164.43'
PORT = '3306'
DATABASE = 'echo-img'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True
