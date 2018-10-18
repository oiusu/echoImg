#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/18 1:57 PM
@desc:
'''
from app import app

# from app.dept import dept
# from app.user import user
from app.echoImg import echoImg


# app.register_blueprint(user, url_prefix='/user')
# app.register_blueprint(dept, url_prefix='/dept')
app.register_blueprint(echoImg, url_prefix='/echoImg')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5031,)
