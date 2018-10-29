#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/18 1:41 PM
@desc:
'''
# from flask import Blueprint, Flask
#
# # app = Blueprint('app', __name__,)
# app = Flask(__name__)
# # from app.user import views

from flask import Flask
import pymysql

from app import config
from app.echoImg.exts import db

pymysql.install_as_MySQLdb()

app = Flask(__name__)
# app.secret_key = "123asdzxc"
app.permanent_session_lifetime=60*60*2
app.config.from_object(config)
db.init_app(app)