# coding:utf-8

import datetime
import hashlib
import os
import time

from PIL import Image
from flask import current_app, jsonify, make_response, send_from_directory, g, request
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from app import photos, files
from ..students.studentModel import StudentInfo
from ...utils.response_code import RET
from ...utils import log


class UploadImageResource(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("Image", type=FileStorage, location="files", required=True, nullable=False,
                            help="Image参数类型不正确或缺失")
        args = parser.parse_args()
        filename = args.get("Image").filename

        # 去掉文件后缀末尾双引号
        ext = filename.rsplit('.', 1)[1].replace("\"", "").replace("\"", "")

        # 对图片保存名称唯一
        key = filename + current_app.config["SECRET_KEY"]
        md5 = hashlib.md5()
        md5.update(key.encode('utf-8'))
        filename = md5.hexdigest()

        try:
            file_name = photos.save(args.get("Image"), folder=None, name=filename + '.' + ext)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.THIRDERR, message="上传图片失败，只支持jpg,png类型")

        # 获得保存后的图片路径
        try:
            image_url = photos.url(file_name)
            base_name = photos.get_basename(file_name).rsplit('.', 1)[0]

            c_url = create_thumbnail(base_name, ext)
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(code=RET.OK, message="图片上传成功", image_url=image_url, c_url=c_url)


class UploadFilesResource(Resource):

    def post(self):
        pass


class DownloadResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("FileName", type=str, location="args", required=True, nullable=False,
                            help="FileName参数类型不正确或缺失")

        args = parser.parse_args()
        filename = args.get("FileName")
        try:
            file_path = os.sep.join(
                [current_app.config['DOWNLOAD_FILES'], str(datetime.datetime.now().strftime('%Y_%m'))])
            response = make_response(send_from_directory(file_path, filename, as_attachment=True))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(
                filename.encode().decode('latin-1'))
            return response
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.IOERR, message="文件下载异常:下载文件不存在")

    # 生成缩略图


def create_thumbnail(filename, ext):
    """
    生成缩略图
    :param filename: 图片的名称
    :param ext: 图片后缀
    :return: 可访问的路径
    """
    from app import photos
    # 生成缩略图
    # pathname = current_app.config['UPLOADED_PHOTOS_DEST'] + "\\" + filename + "." + ext
    pathname = os.sep.join([current_app.config['UPLOADED_PHOTOS_DEST'], filename]) + "." + ext
    # print(pathname)
    # 打开文件
    img = Image.open(pathname)
    # 设置尺寸
    img.thumbnail((128, 128))
    pathname = os.sep.join([current_app.config['UPLOADED_PHOTOS_DEST'], filename]) + "_c." + ext
    # pathname = current_app.config['UPLOADED_PHOTOS_DEST'] + "\\" + filename + "_c." + ext
    # 保存修改后的文件
    img.save(pathname)
    # 获取上传后的文件
    c_url = photos.url(filename + "_c." + ext)
    return c_url


# pandas时间格式转换
def time_convert(time_str):
    if time_str != "":
        time_obj = datetime.datetime.strptime(str(time_str), '%Y-%m-%d')
        time_converted = time_obj.strftime('%Y/%m/%d')
        return time_converted


# 时间戳转换日期格式
def timestamp_to_str(timestamp=None, format='%Y/%m/%d %H:%M:%S'):
    if timestamp:
        time_tuple = time.localtime(timestamp)  # 把时间戳转换成时间元祖
        result = time.strftime(format, time_tuple)  # 把时间元祖转换成格式化好的时间
        return result
    else:
        return time.strptime(format)
