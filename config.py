# coding:utf-8

import os
import datetime


class Config(object):
    """配置信息"""
    SECRET_KEY = "xxx(随便写)"

    # 数据库连接配置
    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'xxx'
    PASSWORD = 'xxx'
    HOST = 'xxx'
    PORT = 'xxx'
    DATABASE = 'xx'

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

     # SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:idealwifi2020@139.9.128.8:13306/paperreview"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 数据库池的大小。 默认与数据库引擎的值相同 (通常为 5)
    SQLALCHEMY_POOL_SIZE = 50

    # 控制连接池达到最大大小后还可以创建的连接数，当这些附加连接返回到连接池时，它们将会被断开并丢弃。
    SQLALCHEMY_MAX_OVERFLOW = 10

    # 上传图片配置
    # linux和windows通用写法
    UPLOADED_PHOTOS_DEST = os.sep.join([os.path.dirname(os.path.realpath(__file__)), 'app', 'static', 'images', 'uploads'])

    # 上传文件的配置
    UPLOADED_FILES_DEST = os.sep.join([os.path.dirname(os.path.realpath(__file__)), 'app', 'static', 'files'])

    # 上传学生模板文件的配置
    UPLOADED_TEMPLATE_DEST = os.sep.join([os.path.dirname(os.path.realpath(__file__)), 'app', 'static', 'files', 'template'])

    # 下载模板文件配置
    DOWNLOAD_FILES = os.sep.join([os.path.dirname(os.path.realpath(__file__)), 'app', 'static', 'files', 'paper', 'master'])

    # token的有效期,单位：秒
    TOKEN_EXPIRES = 3600

    # 图片验证码的redis有效期, 单位：秒
    IMAGE_CODE_REDIS_EXPIRES = 180

    # 系统默认初始密码
    DEFAULT_INITIAL_PASSWORD = 'xxx'

    #查重率
    PASS_DUPLICATE_RATE=0.1


    # RSA公钥public_key
    PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
            -----END PUBLIC KEY-----
            '''

    # RSA密钥private_key
    PRIVATE_KEY = '''-----BEGIN PRIVATE KEY-----
            -----END PRIVATE KEY-----
            '''

class DevelopmentConfig(Config):
    """开发测试模式"""
    DEBUG = True


class ProductConfig(Config):
    """生产环境配置信息"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductConfig
}
