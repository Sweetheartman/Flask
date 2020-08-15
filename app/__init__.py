# coding:utf-8

from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from app.utils.commons import ReConverter
from flask_uploads import UploadSet, configure_uploads
import logging
from logging.handlers import RotatingFileHandler


# 数据库
db = SQLAlchemy()

# 创建redis连接对象
# redis_store = None

# 创建flask_uploads对象
"""
UploadSet第一个参数要和配置文件中的“UPLOADED_PHOTOS_DEST”中间的参数相同，第二个参数可以省略，在配置中添加ALLOW设置
"""
photos = UploadSet('photos', extensions=('jpg', 'png'))
files = UploadSet('files', extensions=('docx', ))
template = UploadSet('template', extensions=('xlsx', 'xls'))
# 配置日志信息
# 设置日志的记录等级
"""
开发应用程序或部署开发环境时，可以使用 DEBUG 或 INFO 级别的日志获取尽可能详细的日志信息来进行开发或部署调试；
应用上线或部署生产环境时，应该使用 WARNING 或 ERROR 或 CRITICAL 级别的日志来降低机器的I/O压力和提高获取错误
日志信息的效率。配置文件为DEBUG时会默认设置级别为DEBUG
"""
logging.basicConfig(level=logging.DEBUG)

# 创建日志记录器，指明日志保存的路径，每个日志文件的最大大小，保存日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)

# 创建日志记录格式
formatter = logging.Formatter('%(asctime)s-%(levelname)s %(filename)s:%(lineno)d %(message)s')

# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)

# 为全局的日志工具对象(flask app使用的)添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式创建app应用对象
def create_app(config_name):
    """
    创建flask的应用对象
    :param config_name: string 配置模式的名字  （"develop", "product"）
    :return:
    """
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    # 使用app初始化db
    db.init_app(app)

    # 初始化redis工具
    # global redis_store
    # redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT,
    #                                 decode_responses=True,
    #                                 password=config_class.REDIS_PASSWORD)

    # 利用Flask_session将数据保存的session中
    Session(app)

    # 为flask补充csrf防护
    # CSRFProtect(app)

    # 为flask-uploads注册app
    # 将 app 的 config 配置注册到 UploadSet 实例 photos,同时初始化
    configure_uploads(app, (photos, files, template))

    # 为flask添加自定义得转换器(放在注册蓝图之前)
    app.url_map.converters["re"] = ReConverter

    # 注册用户Token模块接口蓝图
    from .api_1_0.usertoken import token_api
    app.register_blueprint(token_api, url_prefix="/api/v1.0")

    return app

