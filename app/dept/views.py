#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/18 1:44 PM
@desc:
'''
from app.dept import dept
from flask import jsonify
import json

dept_data = [
    {
        'name': '部门1',
        'id': 12345
    },
    {
        'name': '部门2',
        'id': 12346
    }
]


@dept.route('/<int:id>', methods=['GET', ])
def get(id):
    for dept in dept_data:
        if int(dept['id']) == id:
            return jsonify(status='success', dept=dept)

    return jsonify(status='failed', msg='dept not found')


@dept.route('/depts', methods=['GET', ])
def get_depts():
    data = {
        'status': 'success',
        'depts': dept_data
    }
    return json.dumps(data, ensure_ascii=False, indent=1)
