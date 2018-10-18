#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/18 1:42 PM
@desc:
'''
from flask import Blueprint

echoImg = Blueprint('echoImg', __name__,)

from app.echoImg import views