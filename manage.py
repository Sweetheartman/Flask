#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file: urls
# author: lidekun
# datetime: 2020/4/22 16:39
# software: PyCharm

'''
 this is function  description
'''
# import module your need

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import request, g, jsonify
from app.utils.response_code import RET
from app import create_app
from flask_script import Manager

# 创建flask的app对象
app = create_app("develop")
manager = Manager(app)


# 创建全站拦截器,每个请求之前做处理
@app.before_request
def user_require_token():
    permission = ["common.verifycode", "students.stu_login",
                  "common.apiversion", "common.common_verify",
                  "tutors.tutor_login", "secretary.secretary_login",
                  "platforms.platform_login", "common.common_admin_verify",
                  "professor.professors_login", "paper.papertest", "admin.univisity_login"]
    
    # 如果不是请求login等接口，需要验证token
    if request.endpoint not in permission:
        # 在请求头上拿到token
        token = request.headers.get("Token")
        if not all([token]):
            return jsonify(code=RET.PARAMERR, message="缺少参数Token或请求非法")

        # 校验token格式正确与过期时间（用户未点击退出）
        s = Serializer(app.config["SECRET_KEY"])

        try:
            data = s.loads(token)
        except Exception as e:
            app.logger.error(e)
            # 单平台用户登录失效
            return jsonify(code=RET.SESSIONERR, message='用户未登录或登录已过期')

        # 处理多平台登录的问题
        from app.api_1_0.usertoken.usertokenModel import UserToken
        kwagrs = {
            "id": data['id'],
            "user_type": data['user_type']
        }
        try:
            sql_token = UserToken.get_token(**kwagrs).first().UserToken

        except Exception as e:
            # 校验token是否有效，用户点击退出后该token无效
            return jsonify(code=RET.SESSIONERR, message='用户未登录或登录已过期(已退出)')

        if token != sql_token:
            return jsonify(code=RET.SESSIONERR, message='用户未登录或登录已过期(多平台)')

        # 将用户信息保存到g对象
        result_dict = UserToken.get_user_by_token(sql_token)
        if result_dict['code'] == '200':
            g.user = result_dict['data']
        else:
            return jsonify(code=result_dict['code'], message=result_dict['message'])


# 创建全站拦截器，每个请求之后根据请求方法统一设置返回头
@app.after_request
def process_response(response):
    allow_cors = ['OPTIONS', 'PUT', 'DELETE', 'GET', 'POST']
    if request.method in allow_cors:
        response.headers["Access-Control-Allow-Origin"] = '*'
        if request.headers.get('Origin') and request.headers['Origin'] =='http://paper.ncepu.edu.cn':
            response.headers["Access-Control-Allow-Origin"] = 'http://paper.ncepu.edu.cn'
        if request.headers.get('Origin') and request.headers['Origin'] == 'http://super.paper.ncepu.edu.cn':
            response.headers["Access-Control-Allow-Origin"] = 'http://super.paper.ncepu.edu.cn'

        response.headers["Access-Control-Allow-Credentials"] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST,PUT,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,Token'
        response.headers['Access-Control-Expose-Headers'] = 'VerifyCodeID'
    return response


if __name__ == "__main__":
    manager.run()
