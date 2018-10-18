#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/18 1:44 PM
@desc:
'''
# coding:utf-8
from flask import Blueprint

dept = Blueprint('dept', __name__,)

from app.dept import views