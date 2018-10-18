#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/18 1:44 PM
@desc:
'''

from app.user import user
from flask import jsonify
import json
user_data = [
    {
        'id': 1,
        'name': '张三',
        'age': 23
    },
    {
        'id': 2,
        'name': '李四',
        'age': 24
    }
]


@user.route('/<int:id>', methods=['GET', ])
def get(id):
    for user in user_data:
        if user['id'] == id:
            return jsonify(status='success', user=user)


@user.route('/users', methods=['GET', ])
def users():
    data = {
        'status': 'success',
        'users': user_data
    }
    return json.dumps(data, ensure_ascii=False, indent=1)
