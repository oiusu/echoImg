#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/18 1:42 PM
@desc:
'''
from flask import Blueprint

echoImg = Blueprint('echoImg', __name__,template_folder='templates',static_folder='static',static_url_path='/echoImg')

from app.echoImg import views