#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/29 5:21 PM
@desc:
'''

from functools import wraps
from flask import session, redirect, url_for


# 登录限制的装饰器
def login_required(func):
    @wraps(func)
    def warpper(*args, **kwargs):
        username = session.get("username")
        if username:
            print("[auth] username = %s" % username)
            return func(*args, **kwargs)
        else:
            # return redirect(url_for('login'))
            print("[auth] username = %s" % username)
            return redirect("/echoImg/login")

    return warpper

# def auth(func):
#     def inner(*args,**kwargs):
#         username = session.get("username")
#         if username:
#             print("[auth] username = %s" %username)
#             return func(*args,**kwargs)
#         else:
#             print("[auth] username = %s" % username)
#             return redirect("/echoImg/login")
#
#     return inner