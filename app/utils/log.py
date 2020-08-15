#!/usr/bin/env python
#-*- coding:utf-8 -*-

# file: log
# author: lidekun 
# datetime: 2020/4/24 15:05
# software: PyCharm

def add_user_log(op_type, op_content, op_result):
    """
    添加用户日志
    :param kwargs:用户信息
    :param ip: 用户ip
    :param op_type: 操作类型：1.页面浏览 2.查询数据 3.增加数据 4.修改数据 5.删除数据
    :param op_content: 操作内容
    :param op_result: 操作结果：1--成功；0--失败；
    :return: 正常--True；异常：False
    """
    from ..api_1_0.syslogs.userlogModel import UserLog
    return UserLog.add_user_log(op_type, op_content, op_result)

def add_sys_log(op_type, op_content, op_result, **kwargs):
    """
    添加系统日志
    :param kwargs:用户信息
    :param op_type: 操作类型：操作类型：1:正常登录；2 登录异常（密码出错超出次数）；
                                      3 Ip地址异常；4-非法链接访问 5.页面浏览
                                      6.查询数据 7.增加数据 8.修改数据 9.删除数据
    :param op_content: 操作内容
    :param op_result: 操作结果：1--成功；0--失败；
    :return: 正常--True；异常：False
    """
    from ..api_1_0.syslogs.syslogsModel import SystemLog
    return SystemLog.add_sys_log(op_type, op_content, op_result, **kwargs)