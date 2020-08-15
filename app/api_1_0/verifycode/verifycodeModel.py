#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file: __init__.py
# author: lidekun
# datetime: 2020/4/27 13:02
# software: PyCharm

from sqlalchemy import func
from app import db
from flask import jsonify, current_app
from ...utils.captcha.captcha import captcha
from ...utils.response_code import RET
import datetime
import time



class VerifyCode(db.Model):
    __tablename__ = 'verify_code'

    AutoID = db.Column(db.BigInteger, primary_key=True, info='自增ID')
    VerifyCodeID = db.Column(db.BigInteger, info='业务主键ID(时间+AutoID)')
    VerifyCode = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), info='验证码（4位）')
    IsDeleted = db.Column(db.Integer, server_default=db.FetchedValue(), info='验证码是否有效（默认0）：0--是；1--否')
    CreateTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='添加记录的时间（可用于比对验证码是否过期）')


    @classmethod
    def create_verify_code(cls):

        try:
            # 生成最大ID
            max_id = db.session.query(func.max(cls.AutoID)).first()
            if max_id[0] is None:
                id = 0
            else:
                id = max_id[0]
            verify_code_id = (datetime.datetime.now()).strftime('%Y%m%d') + str(id)
        except Exception as e:
            current_app.logger.error(e)
            return {'code': RET.DBERR, 'message': '数据库异常，生成验证码ID失败', 'error': str(e)}

        try:
            # 生成图片验证码
            name, text, image_data = captcha.generate_captcha()

            # 记录验证码
            verify_code = VerifyCode(
                VerifyCodeID=verify_code_id,
                VerifyCode=text
            )
            db.session.add(verify_code)
            db.session.commit()
        except Exception as e:
            # 错误信息记录日志
            db.session.rollback()
            current_app.logger.error(e)
            return {'code': RET.DBERR, 'message': '数据库异常，生成验证码失败', 'error': str(e)}

        # 返回图片
        return {'code': RET.OK, 'message': 'OK', 'data': image_data, 'verify_code_id': verify_code_id}

    @classmethod
    def check_verify_code(cls, verify_code_id, verify_code):
        """
        校验验证码
        :param verify_code_id: 验证码ID
        :param verify_code: 验证码
        :return:
        """
        try:
            filter_list = []
            filter_list.append(cls.VerifyCodeID == verify_code_id)
            filter_list.append(cls.IsDeleted == 0)
            verify_code_model = db.session.query(cls).filter(*filter_list)
            verify_code_object = verify_code_model.first()

            # 从数据库拿到验证码的值以后就删除
            verify_code_model.update({
                'IsDeleted': 1
            })
            db.session.commit()


            # 如果为空，验证码过期
            if not verify_code_object:
                return {'code': RET.DATAERR, 'message': '验证码已过期', 'error': '验证码已过期'}

            # 检查验证码时间有效性
            verify_code_time = datetime.datetime.strptime(str(verify_code_object.CreateTime), "%Y-%m-%d %H:%M:%S")
            now_time = datetime.datetime.now()

            if (now_time - verify_code_time).seconds > current_app.config['IMAGE_CODE_REDIS_EXPIRES']:
                return {'code': RET.DATAERR, 'message': '验证码已过期', 'error': '验证码已过期'}

            # 检查验证码正确性
            if verify_code_object.VerifyCode != verify_code.upper():
                return {'code': RET.DATAERR, 'message': '验证码不正确', 'error': '验证码不正确'}


            return {'code': RET.OK, 'message': 'OK', 'data': verify_code_object.VerifyCode}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return {'code': RET.DATAERR, 'message': '数据库异常，校验验证码失败', 'error': '数据库异常，校验验证码失败'}
