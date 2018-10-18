#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/18 1:43 PM
@desc:
'''


from flask import Blueprint

user = Blueprint('user', __name__,)

from app.user import views